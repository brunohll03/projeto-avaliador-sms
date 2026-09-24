"""Auditoria reproduzível: compara saídas e separa parecer manual de triagem.
Não altera rótulos originais nem decisões humanas. Rodar após executar.py.
"""
import csv,json,hashlib
from pathlib import Path
from collections import Counter
PASTA=Path(__file__).resolve().parent
PROJETO=PASTA.parent

def ler(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def salvar(p,rows):
    with p.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def main():
    antes=ler(PASTA/'resultados_antes/divergencias.csv')
    novo=ler(PROJETO/'resultados/dataset_gerado.csv')
    esperado={str(c['registro_original']):str(c['esperado']) for c in json.loads((PASTA/'casos_revisados.json').read_text()) if c.get('registro_original')}
    saida=[]
    for r in antes:
        f=r['feature'];i=int(r['registro_original'])-1;n=novo[i][f]
        assert novo[i]['Mensagem']==r['Mensagem']
        status='revisao_manual_pendente';sugestao='';confianca='não conclusivo';metodo='triagem';motivo='Não há parecer individual definitivo. Conferir definição e contexto; discordância não prova erro de nenhuma das partes.'
        if f=='solicita_codigo_autenticacao':
            sugestao=esperado[r['registro_original']];metodo='leitura individual das 121 divergências com PDF p.3';confianca='alta, sujeita à revisão humana'
            if sugestao==r['valor_original']:
                status='falha_script_corrigida'
                motivo='Solicita uso/informação/digitação do código em autenticação, ou apenas atualização de token sem pedir seu valor (registro 946). Regra corrigida conforme contexto.'
            else:
                status='provavel_erro_original'
                motivo='Entrega ou informa um código, sem solicitar seu uso/informação; ou proíbe seu envio. O PDF exige solicitação, não mera presença de código.'
            assert n==sugestao
        elif f=='possui_pix' and r['valor_gerado']=='1':
            status='provavel_erro_original';sugestao='1';confianca='alta';metodo='critério literal PDF p.23'
            motivo='Há menção explícita a Pix fora de URLs. A feature independe de pedir pagamento; transação recebida ou aviso de chave Pix também contam.'
        elif f=='carga_emocional':
            status='diferenca_metodologica';motivo='Categorias geradas por léxico e limites congelados. Não foi fornecida a metodologia original. Não inferir qual rótulo está certo apenas comparando categorias.'
        elif f=='possui_erros_ortografia_gramatica':
            status='validacao_ferramenta_pendente';motivo='LanguageTool e filtros podem errar em marcas, nomes e concordância; informalidade isolada não prova erro. Inspecionar cada alerta antes de decidir.'
        elif f in {'possui_url','possui_url_encurtada','possui_telefone'}:
            status='conferir_criterio_estrutural';motivo={'possui_url':'Domínio sem ponto foi rejeitado; Gov.br foi reconhecido como domínio. Rever política de host/menção antes de mudar rótulo.','possui_url_encurtada':'Lista fixa de cinco serviços; URL curta não basta. Outros encurtadores exigem validar e versionar a lista, não copiar o rótulo original.','possui_telefone':'Validação brasileira exclui número estrangeiro, <NUMERO>, códigos curtos e identificadores. Decidir explicitamente se deseja incluir ramais/serviços curtos ou números dentro de URLs.'}[f]
        elif r['valor_gerado']!=n:
            status='resultado_recalculado';metodo='comparação de resultados, não revisão humana';motivo='Resultado mudou após atualização das regras. Ver detalhes das mudanças e casos de regressão; concordar com o original não é prova independente de correção.'
        saida.append({**r,'valor_gerado_revisado':n,'situacao_analise':status,'valor_sugerido':sugestao,'confianca':confianca,'base_da_analise':metodo,'justificativa_analise':motivo})
    salvar(PASTA/'triagem_divergencias.csv',saida)
    salvar(PASTA/'analise_codigo_autenticacao.csv',[r for r in saida if r['feature']=='solicita_codigo_autenticacao'])
    old=ler(PASTA/'resultados_antes/dataset_gerado.csv');changes=[]
    nomes=[x['nome'] for x in json.loads((PROJETO/'definicoes.json').read_text())]
    for i,(a,b) in enumerate(zip(old,novo),1):
        for f in nomes:
            if a[f]!=b[f]:changes.append(dict(registro_original=i,Mensagem=b['Mensagem'],feature=f,gerado_salvo_antes=a[f],gerado_depois=b[f]))
    salvar(PASTA/'mudancas_resultados.csv',changes)
    m0={r['feature']:r for r in ler(PASTA/'resultados_antes/metricas_por_feature.csv')}
    table=[dict(feature=r['feature'],divergencias_antes=m0[r['feature']]['divergencias'],divergencias_depois=r['divergencias']) for r in ler(PROJETO/'resultados/metricas_por_feature.csv')]
    salvar(PASTA/'resumo_por_feature.csv',table)
    resumo=json.loads((PROJETO/'resultados/resumo_execucao.json').read_text())
    fonte=PROJETO.parent/'dataset_estaticos/DATASET - Dataset_limpo_V1.csv'
    assert hashlib.sha256(fonte.read_bytes()).hexdigest()==json.loads((PASTA/'resultados_antes/resumo_execucao.json').read_text())['referencia_sha256']
    (PASTA/'resumo_auditoria.json').write_text(json.dumps(dict(escopo='Triagem de todas as divergências salvas; leitura individual completa apenas das 121 de autenticação, mais exemplos e limites nas demais features.',antes=len(antes),depois=resumo['divergencias'],concordancia=resumo['concordancia_percentual'],casos_regressao=len(json.loads((PASTA/'casos_revisados.json').read_text())),testes_sinteticos=resumo['testes_alvo_concordantes'],triagem=dict(Counter(r['situacao_analise'] for r in saida)),autenticacao=dict(Counter(r['situacao_analise'] for r in saida if r['feature']=='solicita_codigo_autenticacao'))),ensure_ascii=False,indent=2))
    print((PASTA/'resumo_auditoria.json').read_text())
if __name__=='__main__':main()

"""Executa extração, comparação por célula e testes sintéticos separados.

Uso: python -m classificador_features_sms.notebook_features_final.executar
As decisões humanas existentes são preservadas por ID; jamais corrige a fonte.
"""
from pathlib import Path
import argparse,csv,hashlib,json,sys,unicodedata
from datetime import datetime,timezone
import pandas as pd
import numpy as np
if __package__ in (None,''):
    sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
    from classificador_features_sms.notebook_features_final.classificador import analisar_lote,NOMES,BINARIAS,DEFINICOES,PASTA
else:
    from .classificador import analisar_lote,NOMES,BINARIAS,DEFINICOES,PASTA

CAMPOS_REVISAO=['decisao_humana','valor_decidido','comentario_revisor']
DECISOES={'','original','gerado','outro','inconclusivo'}
CATEGORIAS={'baixo':'baixa','baixa':'baixa','medio':'média','media':'média','alto':'alta','alta':'alta'}

def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def categoria(v):
    limpo=''.join(c for c in unicodedata.normalize('NFKD',str(v).strip().lower()) if not unicodedata.combining(c))
    if limpo not in CATEGORIAS:raise ValueError(f'Categoria emocional desconhecida: {v!r}')
    return CATEGORIAS[limpo]

def canonico(nome,v):
    if nome=='carga_emocional':return categoria(v)
    if str(v).strip() not in {'0','1'}:raise ValueError(f'Valor binário inválido para {nome}: {v!r}')
    return str(v).strip()

def divisao(a,b):return a/b if b else None

def preservar_decisoes(novo,path):
    """Preserva só decisões sobre o mesmo texto/feature/par de valores.

    Decisões de IDs que saíram do relatório permanecem no CSV antigo arquivado.
    Nunca substitui branco por rótulo automático; rejeita decisões inválidas.
    """
    for c in CAMPOS_REVISAO:novo[c]=''
    if not path.exists():return novo
    antigo=pd.read_csv(path,dtype=str,keep_default_na=False)
    exigidos={'id_divergencia',*CAMPOS_REVISAO}
    if not exigidos.issubset(antigo.columns):raise ValueError('Arquivo de revisão perdeu colunas necessárias.')
    if antigo.id_divergencia.duplicated().any():raise ValueError('IDs repetidos na revisão humana.')
    if not set(antigo.decisao_humana).issubset(DECISOES):raise ValueError('Decisão humana inválida. Use original, gerado, outro ou inconclusivo.')
    mapa=antigo.set_index('id_divergencia')
    for i,row in novo.iterrows():
        if row.id_divergencia in mapa.index:
            for c in CAMPOS_REVISAO:novo.at[i,c]=mapa.at[row.id_divergencia,c]
    # Arquiva antes de regenerar: também conserva revisões fora da nova seleção.
    arquivo=path.with_name('revisao_anterior_'+digest(path)[:12]+'.csv')
    if not arquivo.exists():arquivo.write_bytes(path.read_bytes())
    return novo

def validar_revisoes(frame):
    """Não transforma a decisão em alteração no dataset; apenas verifica valores."""
    for row in frame.itertuples():
        if row.decisao_humana not in DECISOES:raise ValueError('Decisão inválida.')
        if row.decisao_humana=='outro':
            if not row.valor_decidido:raise ValueError('Decisão outro exige valor_decidido.')
            canonico(row.feature,row.valor_decidido)
        elif row.valor_decidido and row.decisao_humana in {'original','gerado'}:
            esperado=row.valor_original if row.decisao_humana=='original' else row.valor_gerado
            if canonico(row.feature,row.valor_decidido)!=canonico(row.feature,esperado):
                raise ValueError('valor_decidido conflita com a decisão registrada.')


def executar(origem=None,saida=None):
    origem=Path(origem) if origem else PASTA.parent/'dataset_estaticos/DATASET - Dataset_limpo_V1.csv'
    saida=Path(saida) if saida else PASTA/'resultados'
    saida.mkdir(parents=True,exist_ok=True)
    # Não permite que uma saída canônica sobrescreva a entrada, nem como symlink.
    destinos=['dataset_gerado.csv','comparacao_completa.csv','divergencias.csv','revisao_humana.csv','metricas_por_feature.csv','resultado_testes_sms.csv','testes_todas_features.csv','matriz_carga_emocional.csv','resumo_execucao.json']
    if origem.resolve() in [(saida/n).resolve() for n in destinos]:raise ValueError('A saída sobrescreveria a referência.')
    hash_antes=digest(origem)
    with origem.open(encoding='utf-8-sig',newline='') as arq:
        header=next(csv.reader(arq))
        if len(set(header))!=len(header):raise ValueError('Cabeçalhos duplicados na fonte.')
    df=pd.read_csv(origem,dtype=str,keep_default_na=False)
    if len(df.columns)!=len(set(df.columns)):raise ValueError('Cabeçalhos duplicados.')
    if not {'Mensagem',*NOMES}.issubset(df.columns):raise ValueError('Faltam Mensagem/features na referência.')
    if df.Mensagem.str.strip().eq('').any():raise ValueError('Mensagem vazia na referência.')
    if df.Mensagem.duplicated().any():raise ValueError('Mensagens repetidas: forneça IDs únicos antes de comparar.')
    for n in NOMES:df[n].map(lambda v:canonico(n,v))
    print(f'Classificando {len(df)} mensagens originais, sem modificar a fonte.',flush=True)
    analisados=analisar_lote(df.Mensagem.tolist())
    gerado=df.copy()
    for n in NOMES:gerado[n]=[str(a['features'][n]) for a in analisados]
    gerado['carga_emocional_proporcao']=[a['medida_emocional']['proporcao'] for a in analisados]
    assert gerado.Mensagem.equals(df.Mensagem)
    if 'possivel_golpe' in df:assert gerado.possivel_golpe.equals(df.possivel_golpe)
    referencias={d['nome']:{**d,'pagina_pdf':i+2} for i,d in enumerate(DEFINICOES)}
    difs=[];metricas=[];comparacao=df[['Mensagem']].copy()
    comparacao.insert(0,'registro_original',range(1,len(df)+1))
    for n in NOMES:
        a=df[n].map(lambda v:canonico(n,v));b=gerado[n].map(lambda v:canonico(n,v));igual=a.eq(b)
        comparacao[n+'__original']=df[n];comparacao[n+'__gerado']=gerado[n]
        linha={'feature':n,'mensagens':len(df),'concordancias':int(igual.sum()),'divergencias':int((~igual).sum()),'concordancia_percentual':100*igual.mean()}
        if n in BINARIAS:
            vp=int(((a=='1')&(b=='1')).sum());vn=int(((a=='0')&(b=='0')).sum());fp=int(((a=='0')&(b=='1')).sum());fn=int(((a=='1')&(b=='0')).sum())
            linha.update(VP=vp,VN=vn,FP=fp,FN=fn,precisao=divisao(vp,vp+fp),recall=divisao(vp,vp+fn),F1=divisao(2*vp,2*vp+fp+fn))
        metricas.append(linha)
        for i in df.index[~igual]:
            o=analisados[i];d=referencias[n]
            identificador=hashlib.sha256(json.dumps([df.at[i,'Mensagem'],n,a[i],b[i]],ensure_ascii=False).encode()).hexdigest()[:24]
            difs.append({'id_divergencia':identificador,'registro_original':i+1,'Mensagem':df.at[i,'Mensagem'],'feature':n,
                'valor_original':df.at[i,n],'valor_gerado':gerado.at[i,n],
                'tipo_diferenca':a[i]+' → '+b[i],'pagina_pdf':d['pagina_pdf'],'definicao':d['definicao'],
                'criterio_e_limite':d['limite'],'metodo':o['detalhes'][n]['metodo'],'evidencia_script':o['detalhes'][n]['evidencia'],
                'carga_emocional_proporcao':o['medida_emocional']['proporcao'] if n=='carga_emocional' else ''})
    cols=['id_divergencia','registro_original','Mensagem','feature','valor_original','valor_gerado','tipo_diferenca','pagina_pdf','definicao','criterio_e_limite','metodo','evidencia_script','carga_emocional_proporcao']
    divergencias=pd.DataFrame(difs,columns=cols)
    revisao=preservar_decisoes(divergencias.copy(),saida/'revisao_humana.csv');validar_revisoes(revisao)
    testes=pd.read_csv(PASTA/'testes/sms_teste.csv',dtype=str,keep_default_na=False)
    hash_testes=digest(PASTA/'testes/sms_teste.csv')
    if set(testes.Mensagem)&set(df.Mensagem):raise ValueError('SMS sintético coincide com referência; mantenha os conjuntos separados.')
    print(f'Executando {len(testes)} SMS sintéticos separados.',flush=True)
    testes_analisados=analisar_lote(testes.Mensagem.tolist())
    resultado_testes=testes.copy()
    resultado_testes['obtido']=[str(o['features'][n]) for o,n in zip(testes_analisados,testes.feature_alvo)]
    resultado_testes['concorda']=[canonico(n,a)==canonico(n,b) for n,a,b in zip(testes.feature_alvo,testes.esperado,resultado_testes.obtido)]
    resultado_testes['evidencia_script']=[o['detalhes'][n]['evidencia'] for o,n in zip(testes_analisados,testes.feature_alvo)]
    todas_testes=pd.DataFrame([{'id_teste':row.id_teste,'Mensagem':row.Mensagem,**o['features'],'carga_emocional_proporcao':o['medida_emocional']['proporcao']} for row,o in zip(testes.itertuples(),testes_analisados)])
    for nome,frame in [('dataset_gerado.csv',gerado),('comparacao_completa.csv',comparacao),('divergencias.csv',divergencias),('revisao_humana.csv',revisao),('metricas_por_feature.csv',pd.DataFrame(metricas)),('resultado_testes_sms.csv',resultado_testes),('testes_todas_features.csv',todas_testes)]:
        frame.to_csv(saida/nome,index=False,encoding='utf-8-sig')
    matriz=pd.crosstab(df.carga_emocional.map(categoria),gerado.carga_emocional.map(categoria)).reindex(index=['baixa','média','alta'],columns=['baixa','média','alta'],fill_value=0)
    matriz.to_csv(saida/'matriz_carga_emocional.csv',encoding='utf-8-sig')
    if __package__ in (None,''):
        from classificador_features_sms.notebook_features_final.revisao import gerar_painel
    else:
        from .revisao import gerar_painel
    gerar_painel(revisao,saida/'revisao_divergencias.html')
    assert digest(origem)==hash_antes and digest(PASTA/'testes/sms_teste.csv')==hash_testes
    resumo={'executado_em_utc':datetime.now(timezone.utc).isoformat(),'mensagens_originais':len(df),'features':len(NOMES),'celulas_comparadas':len(df)*len(NOMES),'divergencias':len(difs),'mensagens_com_divergencia':divergencias.registro_original.nunique(),'concordancia_percentual':100*(1-len(difs)/(len(df)*len(NOMES))),
        'sms_sinteticos':len(testes),'testes_alvo_concordantes':int(resultado_testes.concorda.sum()),'testes_alvo_divergentes':int((~resultado_testes.concorda).sum()),'referencia_sha256':hash_antes,'gabarito_sha256':hash_testes,
        'comparacao':'concordância com anotações, não acurácia validada; referência pode conter erros','testes':'casos de desenvolvimento, autorais, não amostra independente de produção','configuracao_emocao':json.loads((PASTA/'configuracao_emocao.json').read_text()),
        'codigo_sha256':{str(p.relative_to(PASTA)):digest(p) for p in PASTA.rglob('*.py') if '__pycache__' not in p.parts}}
    (saida/'resumo_execucao.json').write_text(json.dumps(resumo,ensure_ascii=False,indent=2))
    return resumo,pd.DataFrame(metricas),revisao,resultado_testes

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--origem');parser.add_argument('--saida');args=parser.parse_args()
    r,*_=executar(args.origem,args.saida);print(json.dumps(r,ensure_ascii=False,indent=2))

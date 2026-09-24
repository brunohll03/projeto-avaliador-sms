import unittest,tempfile
from pathlib import Path
import pandas as pd
from ..classificador import analisar_lote,BINARIAS
from ..features.carga_emocional import categorizar,configuracao,medir
from ..executar import preservar_decisoes,validar_revisoes,canonico
from classificador_features_sms.tests.test_classificador import POSITIVOS,NEGATIVOS

class Integridade(unittest.TestCase):
    def test_regressao_definicoes_anteriores(self):
        casos=[(n,POSITIVOS[n],1) for n in BINARIAS]+[(n,t,0) for n in BINARIAS for t in NEGATIVOS[n]]
        outputs=analisar_lote([t for _,t,_ in casos])
        for (n,t,v),o in zip(casos,outputs):
            with self.subTest(feature=n,sms=t):self.assertEqual(o['features'][n],v)

    def test_fronteiras_emocao(self):
        c=configuracao()
        self.assertEqual(categorizar(0),'baixa')
        self.assertEqual(categorizar(c['limite_baixa']),'baixa')
        self.assertEqual(categorizar((c['limite_baixa']+c['limite_media'])/2),'média')
        self.assertEqual(categorizar(c['limite_media']),'média')
        self.assertEqual(categorizar(c['limite_media']+1e-6),'alta')
        self.assertEqual(medir('https://medo.com 123')['proporcao'],0)
        self.assertEqual(medir('Medo e alegria')['proporcao'],2/3)
        with self.assertRaises(ValueError):categorizar(float('nan'))

    def test_preservacao_decisao_e_arquivo_anterior(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'revisao_humana.csv'
            antigo=pd.DataFrame([{'id_divergencia':'abc','decisao_humana':'original','valor_decidido':'0','comentario_revisor':'Revisei com o PDF.'}]);antigo.to_csv(p,index=False)
            novo=pd.DataFrame([{'id_divergencia':'abc'},{'id_divergencia':'novo'}])
            saida=preservar_decisoes(novo,p)
            self.assertEqual(saida.iloc[0].comentario_revisor,'Revisei com o PDF.')
            self.assertEqual(saida.iloc[1].decisao_humana,'')
            self.assertEqual(len(list(Path(tmp).glob('revisao_anterior_*.csv'))),1)

    def test_rotulos_invalidos_nao_viram_zero(self):
        for v in ['', '0.5', '2','desconhecido']:
            with self.assertRaises(ValueError):canonico('possui_url',v)
        self.assertEqual(canonico('carga_emocional','Médio'),'média')
        with self.assertRaises(ValueError):canonico('carga_emocional','0.2')
        row=pd.DataFrame([{'feature':'possui_url','decisao_humana':'outro','valor_decidido':'','valor_original':'0','valor_gerado':'1'}])
        with self.assertRaises(ValueError):validar_revisoes(row)

if __name__=='__main__':unittest.main()

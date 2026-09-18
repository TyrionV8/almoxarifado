"""Obtain only the explicitly listed manufacturer documents; record provenance."""
import urllib.request, urllib.parse, json, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
gh='https://raw.githubusercontent.com/WeActStudio/'
sources={
'pic16f887.pdf':'https://ww1.microchip.com/downloads/en/devicedoc/41291d.pdf',
'pic12f675.pdf':'https://ww1.microchip.com/downloads/en/devicedoc/41190c.pdf',
'pic12f683.pdf':'https://ww1.microchip.com/downloads/en/devicedoc/41211d_.pdf',
'pic12f1501.pdf':'https://ww1.microchip.com/downloads/aemDocuments/documents/OTH/ProductDocuments/DataSheets/40001615C.pdf',
'atmega328p.pdf':'https://docs.arduino.cc/resources/datasheets/ATmega328P-datasheet.pdf',
'uno-pinout.pdf':'https://docs.arduino.cc/resources/pinouts/A000066-full-pinout.pdf',
'nano-pinout.pdf':'https://docs.arduino.cc/resources/pinouts/A000005-full-pinout.pdf',
'stm32f103c8.pdf':gh+'BluePill-Plus/master/Doc/STM32F103C8T6/DS5319-STM32F103x8-Datasheet.pdf',
'stm32g474.pdf':gh+'WeActStudio.STM32G474CoreBoard/master/Doc/STM32G474xE_DS12288.pdf',
'g474-long-schematic.pdf':gh+'WeActStudio.STM32G474CoreBoard/master/Hardware/QFN48/WeAct-STM32G474CoreBoard_Long/WeAct-STM32G474CoreBoard_Long_V10 SchDoc.pdf',
'g474-long-pinout.pdf':gh+'WeActStudio.STM32G474CoreBoard/master/Hardware/QFN48/WeAct-STM32G474CoreBoard_Long/WeAct-STM32G474CoreBoard_Long_V10 Board Shape 外形.pdf',
'stm32h7r3.pdf':gh+'WeActStudio.STM32H7R3Zx_CoreBoard/master/Doc/stm32h7r3z8.pdf',
'h7-schematic.pdf':gh+'WeActStudio.STM32H7R3Zx_CoreBoard/master/Hardware/WeAct-STM32H7R3Zx_CoreBoard_V10 SchDoc.pdf',
'h7-pinout.pdf':gh+'WeActStudio.STM32H7R3Zx_CoreBoard/master/Hardware/WeAct-STM32H7R3Zx_CoreBoard_V10 Board Shape 外形.pdf',
'stm32f411ce.pdf':gh+'WeActStudio.MiniSTM32F4x1/master/Datasheet/STM32F411CEU6_Datasheet.pdf',
'blackpill-pinout.pdf':gh+'WeActStudio.MiniSTM32F4x1/master/General document/STM32F4x1 v2.0+ Pin Layout.pdf',
'stm32h743vi.pdf':gh+'MiniSTM32H7xx/master/Datasheet/MCU/STM32H743VI_Datasheet.pdf',
'h743-schematic.pdf':gh+'MiniSTM32H7xx/master/Hardware/STM32H7xx SchDoc V12.pdf',
'h743-pinout.pdf':gh+'MiniSTM32H7xx/master/Hardware/STM32H7xx_BoardShape Board Shape 外形 V12.pdf',
}
# Data de obtenção de cada arquivo; os demais vieram em 12/09/2026.
retrieved={'stm32h743vi.pdf':'2026-09-17','h743-schematic.pdf':'2026-09-17','h743-pinout.pdf':'2026-09-17',
 'weact-h743-boardshape.png':'2026-09-17'}
# Desenhos de pinagem que não existem em PDF oficial. Licença e crédito são obrigatórios na exibição.
pinouts={
'bluepill-generic-f103.png':dict(
 url='https://upload.wikimedia.org/wikipedia/commons/9/90/Stm32f103_pinout_diagram.png',
 credit='Rasmus Friis Kjeldsen · reblag.dk/stm32',license='CC BY-SA 4.0',
 note='Diagrama genérico STM32F103 publicado no Wikimedia Commons.'),
'weact-g474-long-board.png':dict(
 url=gh+'WeActStudio.STM32G474CoreBoard/master/Images/1.png',
 credit='WeAct Studio',license='Documentação do fabricante da placa',
 note='Render oficial da versão Long com os nomes dos pinos.'),
'weact-h7r3-board.png':dict(
 url=gh+'WeActStudio.STM32H7R3Zx_CoreBoard/master/Images/1.png',
 credit='WeAct Studio',license='Documentação do fabricante da placa',
 note='Render oficial da placa H7R3 com os nomes dos pinos.'),
'weact-h743-boardshape.png':dict(
 url=gh+'MiniSTM32H7xx/master/Images/BoardShape.png',
 credit='WeAct Studio',license='Documentação do fabricante da placa',
 note='Desenho mecânico da MiniSTM32H7xx (40,64 × 66,88 mm); referência de posição para os desenhos da H743.'),
}
def fetch(path,url,magic):
 if not path.exists():
  payload=urllib.request.urlopen(urllib.request.Request(urllib.parse.quote(url,safe=':/+'),headers={'User-Agent':'almoxarifado/1.0'}),timeout=45).read()
  if not payload.startswith(magic): raise ValueError('Conteúdo inesperado')
  path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(payload)
 return hashlib.sha256(path.read_bytes()).hexdigest()
manifest=[]
images=[]
failures=[]
for name,url in sources.items():
 path=ROOT/'assets/documents'/name
 try:
  manifest.append(dict(file=str(path.relative_to(ROOT)),url=url,sha256=fetch(path,url,b'%PDF'),retrieved=retrieved.get(name,'2026-09-12')))
  print(name,path.stat().st_size,flush=True)
 except Exception as e:
  failures.append(name);print('FAILED',name,str(e),flush=True)
for name,meta in pinouts.items():
 path=ROOT/'assets/pinouts/sources'/name
 try:
  images.append(dict(file=str(path.relative_to(ROOT)),sha256=fetch(path,meta['url'],b'\x89PNG\r\n\x1a\n'),retrieved=retrieved.get(name,'2026-09-12'),**meta))
  print(name,path.stat().st_size,flush=True)
 except Exception as e:
  failures.append(name);print('FAILED',name,str(e),flush=True)
if failures: raise SystemExit('Downloads incompletos; manifesto anterior preservado: '+', '.join(failures))
(ROOT/'data/sources.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
(ROOT/'data/pinout_sources.json').write_text(json.dumps(images,ensure_ascii=False,indent=2)+'\n')

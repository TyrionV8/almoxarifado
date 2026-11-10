# ▦ Almoxarifado

**Conheça o que você tem. Escolha o que seu projeto precisa.**

Seu acervo de microcontroladores, lógica programável e periféricos, com comparação lado a lado, mapas de pinagem e documentação de bancada. Local, sem conta e sem instalação.

## Abrir

Clone este repositório e abra **[index.html](index.html)** no navegador. É só isso — não precisa iniciar servidor, instalar pacotes ou criar banco.

Para receber melhorias, execute `git pull` na pasta do projeto e recarregue a página.

## Registrar compras, uso e descartes

Comprou mais, colocou uma placa num projeto ou queimou uma? No terminal, dentro da pasta do projeto:

```bash
python3 scripts/server.py
```

O navegador abre o almoxarifado com a aba **Histórico** liberada: escolha o que aconteceu, a quantidade, a data e, se quiser, uma observação. O registro vai direto para o banco. Depois é só comitar a pasta `data/`. Aberto pelo `index.html`, o histórico aparece apenas para consulta.

## Na bancada

- **14 modelos em três setores:** 11 microcontroladores; a Sipeed Tang Nano 9K em **Lógica programável**; e a tela LCD de 4,3″ (480 × 272) e a câmera WeAct M12 em **Periféricos**. LCD significa tela de cristal líquido. A câmera ainda tem sensor a confirmar. A quantidade aparece como **disponíveis/total** e cada item tem seu histórico. As unidades PIC são estimativas do Obsidian.
- **Compare:** marque os componentes na tabela; as diferenças aparecem destacadas.
- **Explore:** expanda uma linha para ver especificações, aplicação, pinagem e datasheet.
- **Entenda:** 111 termos organizados por assunto, com nome completo das siglas, explicação simples, funcionamento e exemplo do acervo. A aba **Documentação** também traz esquemas clicáveis e um guia para interpretar fichas técnicas. Funciona por mouse, teclado e toque.
- **Consulte offline:** documentos originais e leitura comentada incluídos no repositório. Links para as fontes são opcionais e precisam de internet.
- **Conecte:** fichas do CH343P, ST-Link V2 e PICkit 3.

A BlackPill cadastrada é a **WeAct STM32F411CEU6, cristal de 25 MHz e Flash externa de 8 MB**, usada no TCC (Trabalho de Conclusão de Curso). As três BluePill são STM32F103C8T6 (duas USB-C, uma micro-USB). Uno e Nano usam as referências clássicas ATmega328P.

A H743 do kit H743-LCD-M12 é a mesma unidade já cadastrada; seu estoque não foi duplicado. A tela de 0,96″ permanece como recurso da placa. A Tang Nano 9K usa uma **FPGA** (Field-Programmable Gate Array, matriz lógica programável), com seis folhas novas de pinagem e conexão no padrão simples/completo do acervo. Identificação e fontes: [compras de 26/10/2026](docs/COMPRAS-2026-10-26.md).

## Como os dados ficam guardados

O **SQLite** é um banco de dados em um único arquivo: [data/inventory.sqlite](data/inventory.sqlite). A página lê uma cópia gerada desse banco, permitindo abrir diretamente pelo arquivo, sem servidor. Banco, cópia de leitura e documentos são versionados juntos. Colunas da tabela, campos das fichas e categorias da documentação também vêm do banco.

As alterações permanentes são feitas no projeto e compartilhadas por `commit`, `push` e `pull` — registrar, enviar e receber versões no Git. A seleção para comparar é temporária. Só o servidor local (`scripts/server.py`) grava no banco, e apenas movimentações de unidades.

A leitura comentada destaca os **termos cadastrados**; ela não traduz automaticamente todo o documento. Para desenhos, tabelas complexas e limites elétricos completos, use a aba do documento original.

## Continuar o desenvolvimento

Peça ao próximo agente: **“Leia o handoff.md antes de alterar o projeto.”**

O [handoff.md](handoff.md) registra arquitetura, fontes, decisões, testes, manutenção e pendências. Créditos dos documentos: [docs/SOURCES.md](docs/SOURCES.md).

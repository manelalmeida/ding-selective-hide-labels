# DING Selective Hide App Labels

**Português (Portugal)** | [English](README.md)

Utilitário leve e atalho para a extensão **Desktop Icons NG (DING)** no GNOME Shell que oculta seletivamente os nomes apenas dos atalhos de aplicações (ficheiros `.desktop`) no ambiente de trabalho, mantendo os nomes visíveis de pastas e ficheiros normais.

---

## Modo de Funcionamento

A extensão DING apenas disponibiliza uma opção global para mostrar ou ocultar os nomes de todos os ícones em simultâneo. Para ocultar seletivamente apenas os nomes das aplicações sem alterar o código-fonte da extensão:

1. **Filtragem seletiva (apenas `*.desktop`):** Ao ser executado, o `ocultar_nomes.py` analisa a pasta do ambiente de trabalho (`xdg-user-dir DESKTOP`, normalmente `~/Desktop`) e atua exclusivamente sobre ficheiros `.desktop`. Pastas e documentos normais são completamente ignorados.
2. **Substituição por *Zero-Width Space* (`\u200b`):** Dentro da secção `[Desktop Entry]` de cada ficheiro `.desktop`, o script substitui `Name=` (e variantes localizadas `Name[...]=`) por uma sequência crescente de caracteres Unicode *Zero-Width Space* (`\u200b`) (`2x`, `3x`, `4x`, etc.).
   * Ao contrário de espaços normais, o carácter `\u200b` não é ignorado pelo DING.
   * Como tem largura visual nula, sequências longas nunca provocam quebra de linha nem truncagem com reticências (`...`).
   * Atribuir um comprimento diferente a cada ficheiro evita que o DING detete nomes duplicados.
3. **Backup automático:** Antes de alterar qualquer atalho que ainda tenha um nome visível, as linhas originais `Name=` e `Name[...]=` são guardadas em `~/.local/share/ding-hide-labels/backup.json`.
4. **Recarregamento imediato da extensão:** Após atualizar os ficheiros, o script reinicia a extensão `ding@rastersoft.com` através do comando `gnome-extensions` para aplicar as alterações no ecrã de imediato.
5. **Restauro inteligente (`restaurar_nomes.py`):** Repõe os nomes originais a partir do `backup.json`. Caso um atalho já estivesse sem nome antes do primeiro backup, o script procura automaticamente o ficheiro `.desktop` original nas pastas de aplicações do sistema e Flatpak (`/usr/share/applications`, `/var/lib/flatpak/exports/share/applications`, `~/.local/share/...`).

---

## Requisitos

* Ambiente gráfico **GNOME Shell** com a extensão **Desktop Icons NG (DING)** (`ding@rastersoft.com`) instalada e ativa.
* **Python 3** (pré-instalado no Fedora, Ubuntu e na maioria das distribuições modernas).
* Ferramentas de linha de comandos `gio` e `gnome-extensions` (incluídas no GNOME).

---

## Instalação

1. **Clonar o repositório:**
   ```bash
   git clone [https://github.com/manelalmeida/ding-selective-hide-labels.git](https://github.com/manelalmeida/ding-selective-hide-labels.git)
   cd ding-selective-hide-labels
Executar o instalador:

Bash
chmod +x install.sh
./install.sh
O que o install.sh faz:
Copia os scripts ocultar_nomes.py e restaurar_nomes.py para ~/.local/bin/.

Cria um atalho clicável sem nome (ocultar-nomes.desktop) no ambiente de trabalho com permissões 0755 e marca-o como confiável através de gio set ... metadata::trusted true.

Executa o ocultar_nomes.py de imediato para ocultar os nomes das aplicações existentes.

Utilização
Ocultar nomes de novas aplicações: Sempre que adicionares um novo atalho de aplicação ao ambiente de trabalho, clica no ícone de atualização (view-refresh) no ambiente de trabalho para ocultar o nome e recarregar o DING.

Repor os nomes originais das aplicações (sem desinstalar):

Bash
~/.local/bin/restaurar-nomes.py
Desinstalação
Para remover os scripts, o atalho do ambiente de trabalho e o backup local:

Bash
cd ding-selective-hide-labels
chmod +x uninstall.sh
./uninstall.sh
O desinstalador pergunta se pretendes restaurar os nomes originais das aplicações antes de apagar os ficheiros.

Limitações Conhecidas
Ícone nativo do Lixo (Trash): O ícone do Lixo fornecido pelo DING é gerado internamente pela extensão e não a partir de um ficheiro .desktop em ~/Desktop, pelo que o seu nome não é ocultado por este script. Como alternativa, podes desativar o ícone nativo do Lixo nas definições do DING e criar um atalho .desktop personalizado com Exec=gio open trash:///.

# DING Selective Hide App Labels

Script e atalho para a extensão **Desktop Icons NG (DING)** no GNOME que ocultam seletivamente os nomes apenas dos atalhos de aplicações (`.desktop`) no ambiente de trabalho, mantendo pastas e ficheiros normais com os respetivos nomes.

## Funcionalidades
- Oculta os nomes apenas de ficheiros `*.desktop` no ambiente de trabalho usando quantidades crescentes de *Zero-Width Space* (`\u200b`), evitando `...` e colisões de nomes iguais no DING.
- Guarda automaticamente os nomes originais em `~/.local/share/ding-hide-labels/backup.json`.
- Inclui script de restauro (`restaurar_nomes.py`) com recuperação automática via backup ou ficheiros `.desktop` do sistema/Flatpak.
- Cria um atalho clicável sem nome no ambiente de trabalho para reexecutar quando adicionares novas apps.

## Instalação
```bash
git clone [https://github.com/manelalmeida/ding-selective-hide-labels.git](https://github.com/manelalmeida/ding-selective-hide-labels.git)
cd ding-selective-hide-labels
./install.sh


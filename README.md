# Ganso Cursor 🪿

Um script em Python que cria um ganso animado flutuante na tela. O ganso persegue o cursor do mouse pela área de trabalho e foge até a borda da tela ao ser capturado.

Desenvolvido com renderização vetorial no **Pygame** e chamadas nativas da **Win32 API** para sobreposição em nível de sistema no Windows.

---

## 🚀 Funcionalidades

- **Sem imagens externas:** Toda a arte do ganso e suas animações de caminhada são desenhadas dinamicamente via código.
- **Transparência total:** Apenas o ganso é visível na tela; o fundo permanece transparente e clicável.
- **Injeção DWM (Topmost Absoluto):** Utiliza a API `SetWindowBand` do Windows para garantir prioridade de exibição na camada superior.
- **Interativo:** Foge do mouse e arrasta o ponteiro para as bordas da tela ao interceptá-lo.

---

## 📋 Pré-requisitos

Certifique-se de ter o Python 3 instalado juntamente com as bibliotecas necessárias:

```bash
pip install pygame pyautogui pynput
⚙️ Como Executar
Como o script faz uso da chamada nativa SetWindowBand para garantir exibição acima de janelas protegidas do sistema, ele deve ser executado em um terminal como Administrador.

Abra o Prompt de Comando ou PowerShell como Administrador.

Execute o comando:

DOS
python "D:\apps\Ganso Cursor\ganso.pyw"
🛑 Como Encerrar o Script
Você pode encerrar o ganso a qualquer momento utilizando um dos métodos abaixo:

Atalho de emergência (Teclado): Digite as letras p a r a em sequência em qualquer lugar da tela.

Trava de segurança (FailSafe): Mova rapidamente o cursor do mouse para o canto superior esquerdo extremo do monitor (coordenadas 0,0).

Tecla ESC: Caso a janela receba foco direto.

Terminal: Pressione Ctrl + C na janela do terminal aberta.

🛠️ Tecnologias Utilizadas
Python 3

Pygame (renderização gráfica e controle de frames)

PyAutoGUI (leitura de posição do cursor)

pynput (listener de atalhos globais de teclado/mouse)

ctypes / Win32 API (gerenciamento de janelas e camadas do Windows DWM)
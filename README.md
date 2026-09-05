# Snake - Jogo da Cobrinha

Jogo Snake desenvolvido em Python utilizando a biblioteca Pygame. O jogador controla a cobra, coleta alimentos, aumenta sua pontuacao e deve evitar as bordas da tela e o proprio corpo.

## Requisitos

- Python 3.10 ou superior
- Pygame
- Windows ou Linux (incluindo WSL com suporte grafico)

## Como executar

1. (Opcional) Crie e ative um ambiente virtual:

   ```bash
   python -m venv .venv
   # Linux/macOS
   source .venv/bin/activate
   # Windows PowerShell: .venv\Scripts\Activate.ps1
   ```

2. Instale a dependencia:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Inicie o jogo:

   ```bash
   python snake_game.py
   ```

## Controles

- Setas direcionais ou `W`, `A`, `S`, `D`: movimentar a cobra
- Botao `INICIAR` ou `Enter`: iniciar o jogo na tela inicial
- `R` ou `Enter`: reiniciar depois do Game Over
- Fechar a janela: sair do jogo

O jogo inicia em uma janela fixa de 720 x 592 pixels, sem permitir redimensionamento. A cada alimento coletado, a cobra cresce e a pontuacao aumenta em um ponto.

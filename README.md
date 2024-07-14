
# Art Gallery

Este é um projeto da disciplina Algoritmos 2, ministrada pelo professor Renato Vimiero. O projeto foi desenvolvido pelos alunos Diogo Tuler, João Marcos Tomaz e Rafael Martins.

## Ideia do Projeto

O projeto diz respeito a solucionar o Problema da Galeria de Arte. Dada uma galeria de arte (aqui representada por um polígono), queremos encontrar o menor número de câmeras que cubram todo o espaço da galeria, i.e., todos os lados do polígono.

## Como Executar

Para executar o projeto localmente, siga estas instruções:

1. Clone o repositório:

   ```bash
   git clone https://github.com/joaomarcostomaz/Art_Gallery.github.io.git

2. Navegue até o diretório do projeto:

   ```bash
   cd Art_Gallery.github.io/

3. Crie e ative um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv       # Cria o ambiente virtual
   source venv/bin/activate  # Ativa o ambiente virtual (Linux/macOS)
   # Ou no Windows use: venv\Scripts\activate

4. Instale as dependências necessárias:
   ```bash
   pip install -r requirements.txt

5. Inicie a aplicação:
   ```bash
   python -m src.app

6. Abra um navegador e acesse http://localhost:8051/ para utilizar. Caso essa porta esteja ocupada é necessário alterar o código no arquivo app.py para rodar em uma porta livre:
   ```bash
   if __name__ == '__main__':
    print("Starting the Dash app server...")
    app.run_server(debug=True,port=8051) # Mude a porta aqui

## Acesso à Página no Github Pages

Para uma visualização dinâmica e interativa do relatório completo e dos processos abordados em nosso trabalho, você pode acessar o GitHub Pages através do seguinte link:[https://joaomarcostomaz.github.io/Art_Gallery.github.io/](https://joaomarcostomaz.github.io/Art_Gallery.github.io/).

# Projeto-Status-de-Comunicacao

Descrição
- Este projeto foi desenvolvido para a Sotreq S/A com o objetivo de automatizar a verificação e atualização de datas de comunicação em planilhas Excel. O código, escrito em Python, busca números de série específicos, mesmo quando combinados em uma única célula, e atualiza as datas automaticamente se forem mais recentes. Isso elimina a necessidade de verificação manual, economizando tempo e reduzindo erros.

Objetivo:
- O principal objetivo deste projeto é automatizar o processo de verificação e atualização de datas em planilhas Excel, garantindo que todas as informações sejam precisas e atualizadas sem a necessidade de intervenção manual. Essa automação visa aumentar a eficiência e a precisão das operações na Sotreq S/A.


Funcionalidades:
- Leitura e Manipulação de Planilhas Excel: Utiliza a biblioteca pandas para ler, manipular e atualizar dados em planilhas Excel.
- Automação Web com Selenium: A biblioteca selenium é utilizada para acessar uma interface web, buscar informações específicas (datas de comunicação), e integrá-las com os dados do Excel.
- Tratamento de Números de Série Combinados: O código é capaz de identificar e tratar números de série que aparecem combinados em uma célula, como "ABC00000 / ABC11111"(fictícios para exemplo).
- Atualização Condicional de Dados: As datas são atualizadas automaticamente na planilha, desde que a data obtida na web seja mais recente do que a data atual na planilha.
- Gerenciamento de Variáveis de Ambiente: O projeto utiliza a biblioteca dotenv para gerenciar variáveis de ambiente, facilitando a configuração de caminhos e outras variáveis necessárias para o processamento e automação.


Tecnologias Utilizadas
- Python: Linguagem principal utilizada para o desenvolvimento do projeto.
- Pandas: Biblioteca usada para manipulação e análise de dados em planilhas Excel.
- Selenium: Biblioteca utilizada para automação da interação com a interface web.
- OS: Biblioteca padrão do Python utilizada para interação com o sistema operacional, como manipulação de caminhos e variáveis de ambiente.
- Dotenv: Biblioteca utilizada para carregar variáveis de ambiente a partir de um arquivo .env, facilitando a configuração do ambiente de desenvolvimento.


Estrutura do Projet:
- processamento_dados.py: Contém as funções que processam os dados das planilhas Excel e identificam as entradas que precisam ser atualizadas.
- dsp_automation.py: Contém a lógica de automação web usando Selenium para buscar as datas mais recentes.
- main.py: Arquivo principal que orquestra a execução das funções de processamento e automação.


Como Funciona -

1 - Processamento de Dados:
- O script processamento_dados.py é responsável por ler as planilhas Excel, identificar os números de série e verificar se as datas precisam ser atualizadas.
Números de série combinados em uma célula são tratados adequadamente, garantindo que cada número seja considerado individualmente.


2 - Automação Web:
- O script dsp_automation.py usa Selenium para acessar uma interface web, buscar os números de série que precisam ser atualizados e extrair a data de comunicação mais recente.
A data extraída é então comparada com a data existente na planilha, e a planilha é atualizada se a nova data for mais recente.


3 - Execução Principal:
- O arquivo main.py reúne as funções de processamento e automação, coordenando a execução do fluxo completo do projeto.




Resultados:
- Eficiência: A automação deste processo reduziu significativamente o tempo gasto em tarefas manuais e diminuiu a margem de erro, garantindo que as informações estejam sempre atualizadas.
- Escalabilidade: O projeto foi desenvolvido de forma modular, permitindo fácil adaptação para diferentes planilhas e necessidades futuras.

Contribuição:
- Se você tiver sugestões, melhorias ou encontrar bugs, sinta-se à vontade para abrir uma issue ou enviar um pull request.




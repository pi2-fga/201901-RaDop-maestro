# Maestro

O **Maestro** é o serviço do projeto RaDop responsável por orquestrar todos os serviços e microsserviços que serão usados em conjunto com o radar, o *Dashboard* e o RaDop App.

## Comandos básicos

### Iniciar o RabbitMQ

- caso ele esteja instalado na máquina:

`rabbitmq`

- caso esteja usando o docker do RabbitMQ:

`# docker run -p 5672:5672 rabbitmq:3-alpine`

### Iniciar o maestro

- com o RabbitMQ já em execução, digite o seguinte comando a partir da pasta **maestro**:

`$ python queue_worker.py`

## Parâmetros das Mensagens

Para a mensagem ser corretamente recebida e processada pelo maestro, o payload da mensagem deve estar no formato JSON (**com as chaves entre aspas simples(') ou duplas (")**. Do contrário, haverá erro e o JSON não poderá ser processado) e ter as seguintes chaves:

- **type:** String com o tipo de payload que foi enviado. Esse tipo é usado para o maestro determinar o que ele deverá fazer com os dados recebidos;
- **payload:** O conteúdo em si do payload. Deve ser uma string, mas pode ser um outro JSON.

No arquivo `examples/message_queue.py`, há um exemplo de script para fazer a conexão com a fila de mensagens do RabbitMQ e enviar a mensagem desejada.

## Tecnologias Utilizadas

- Python 3
- [Pika (Python 3)](https://github.com/pika/pika/)
- Docker

## Ambiente de Desenvolvimento

Para evoluções e desenvolvimento basta ter instalado em sua máquina o Python 3 e as demais dependências do projeto (que são explicadas logo a baixo), além do seu editor de texto de preferência.

## Ambiente de Testes Local

Antes da instalação das ferramentas de ambiente, certifique-se de que você tem o *message broker* [RabbitMQ](https://www.rabbitmq.com/) rodando para a realização dos testes.

Recomendados a utilização de um ambiente virtual criado pelo módulo `virtualenvwrapper`.
Existe um sítio virtual com instruções em inglês para a instalação que pode ser acessado [aqui](https://virtualenvwrapper.readthedocs.io/en/latest/install.html). Mas você pode também seguir o roteiro abaixo para a instalação do ambiente:

```shell
sudo python3 -m pip install -U pip             # Faz a atualização do pip
sudo python3 -m pip install virtualenvwrapper  # Caso queira instalar apenas para o usuário use a opt --user
```

Agora configure o seu shell para utilizar o virtualenvwrapper, adicionando essas duas linhas ao arquivo de inicialização do seu shell (`.bashrc`, `.profile`, etc.)

```shell
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
```

Caso queira adicionar um local específico de projeto basta adicionar uma terceira linha com o seguinte `export`:

```shell
export PROJECT_HOME=/path/to/project
```

Execute o arquivo de inicialização do shell para que as mudanças surtam efeito, por exemplo:

```shell
source ~/.bashrc
```

Agora crie um ambiente virtual com o seguinte comando (colocando o nome que deseja para o ambiente), neste exemplo usarei o nome composta:

```shell
mkvirtualenv maestro
```

Para utilizá-lo:

```shell
workon maestro
pip install -r requirements.txt   # Irá instalar todas as dependências usadas no projeto
```

## Build

Para construir e rodar o container do maestro basta rodar os seguintes comandos:

```
docker build -t maestro:latest .
docker run -d --name maestro --net=host maestro
```


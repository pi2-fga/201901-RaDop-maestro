# Maestro

O **Maestro** é o serviço do projeto RaDop responsável por orquestrar todos os serviços e microsserviços que serão usados em conjunto com o radar, o *Dashboard* e o RaDop App.

## Comandos básicos

O Maestro funciona em conjunto com o _message broker_ RabbitMQ para o recebimento de dados. Por isso, para que aquele possa funcionar, é necessário que o RabbitMQ esteja em execução.

### Iniciar o RabbitMQ

- caso ele esteja instalado na máquina:

`rabbitmq`

- caso esteja usando o docker do RabbitMQ:

`# docker run -p 5672:5672 --net=host rabbitmq:3-alpine`

### Iniciar o maestro

- com o RabbitMQ já em execução, digite o seguinte comando a partir da pasta **/src**:

`$ python main.py`

## Parâmetros das Mensagens

Para que o Maestro possa receber as mensagens vindas do RabbitMQ, é necessário que a fila seja corretamente configurada, com os seguintes parâmetros:
- **queue:** `maestro`;
- **routing_key:** `message.maestro`;
- **exchange_type:** `topic`.

Exemplos de como configurar o envio de mensagens, com esses parâmetros, podem ser encontrados na pasta `/examples`.

Para a mensagem ser corretamente recebida e processada pelo Maestro, o *payload* da mensagem do RabbitMQ deve estar no formato JSON (**com as chaves entre aspas simples(') ou duplas (")**. Do contrário, haverá erro e o JSON não poderá ser processado).

Os parâmetros que deverão ser passados são diferentes dependendo do tipo de mensagem sendo passada, estando listados nos subtópicos a seguir:

### Infração

O JSON da infração deve conter as seguintes chaves:
- **id:** id: Um UUID para identificar unicamente aquele pacote (tipo `string`);
- **type:** Tipo de chamada da função, para que o Maestro possa determinar o que deve ser feito com os dados que foram recebidos. Neste caso, o tipo **deve** ter o valor `vehicle-flagrant` (tipo `string`);
- **payload:** É um outro JSON contendo os dados da infração em si. ele deve ter as seguintes chaves:
  - **id_radar:** Identificador único do radar que enviou os dados (tipo `number`);
  - **image1:** Imagem do veículo infrator no momento flagrante, codificada em **base64** (tipo `string`);
  - **image2:** Imagem alternativa do veículo infrator no momento flagrante, codificada em **base64** (tipo `string`);
  - **infraction:** Código da infração que foi cometida pelo veículo (tipo `number`);
  - **vehicle_speed:** Velocidade do carro que foi medida pelo radar (tipo `number`);
  - **considered_speed:** Velocidade considerada do veículo, tendo em conta a margem de erro da medição do radar (tipo `number`);
  - **max_allowed_speed:** Velocidade máxima permitida na via na qual o radar está instalado (tipo `number`).
- **time:** O dia e horário em que essa mensagem foi enviada, no formato RFC3339, ou seja, YYYY-MM-DDTHH:MM:SSZ (tipo `string`).

**Exemplo:**
```
{
    "id": "44b314eb-b67d-4b4f-b744-4772c5954601",
    "type": "vehicle-flagrant",
    "payload":{
        "id_radar": 4,
        "image1": "base64",
        "image2": "base64",
        "infraction": 2,
        "vehicle_speed": 80,
        "considered_speed": 77,
        "max_allowed_speed": 60
    },
    "time": "2019-06-07T19:24:04.102394Z"
}
```

No arquivo `vehicle_flagrant_msg.py` na pasta `/examples` há um exemplo de script para fazer a conexão com a fila de mensagens do RabbitMQ e enviar uma mensagem de uma infração.


### Status do radar

O JSON do status do radar deve conter as seguintes chaves:
- **id:** id: Um UUID para identificar unicamente aquele pacote (tipo `string`);
- **type:** Tipo de chamada da função, para que o Maestro possa determinar o que deve ser feito com os dados que foram recebidos. Neste caso, o tipo **deve** ter o valor `status-radar` (tipo `string`);
- **payload:** É um outro JSON contendo os dados da infração em si. ele deve ter as seguintes chaves:
  - **radar_id:** Identificador único do radar que enviou os dados (tipo `number`);
  - **radar:** Código do status de funcionamento do radar (tipo `number`);
  - **camera:** Código do status de funcionamento da câmera do radar (tipo `number`);
  - **rasp:** Código do status de funcionamento da Raspberry Pi do radar (tipo `number`);
  - **rasp:** Código do status de funcionamento da USPR do radar (tipo `number`);
  - **time:** O dia e horário em que esses dados do funcionamento do radar foram obtidos, no formato RFC3339, ou seja, YYYY-MM-DDTHH:MM:SSZ (tipo `string`)
- **time:** O dia e horário em que essa mensagem foi enviada, no formato RFC3339, ou seja, YYYY-MM-DDTHH:MM:SSZ (tipo `string`).

**Exemplo:**
```
{
    "id": "44b314eb-b67d-4b4f-b744-4772c5954601",
    "type": "status-radar",
    "payload": {
        "radar_id": 4,
        "radar": 1,
        "camera": 0,
        "rasp": 1,
        "uspr": 1,
    },
    "time": "2019-06-07T19:24:04.102394Z"
}
```

No arquivo `status_radar_msg.py` na pasta `/examples` há um exemplo de script para fazer a conexão com a fila de mensagens do RabbitMQ e enviar uma mensagem contendo as informações do funcionamento do radar.

## Tecnologias Utilizadas

- Python 3
- [Pika (Python 3)](https://github.com/pika/pika/)
- Docker
- [RabbitMQ](https://www.rabbitmq.com/)

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


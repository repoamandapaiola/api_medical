# Api Medical
api para obter prescrições médicas

# Requisitos

> OK - O serviço de prescrição deverá persistir no banco de dados somente os atributos recebidos no request; <br>
> OK - Os serviços dependentes deverão ser consultados para compor os dados a serem enviados ao serviço de métricas; <br>
> OK - Se o serviço de clínicas não responder, o request deverá seguir normalmente, pois o nome da clínica é o único atributo não obrigatório do serviço de métricas; <br>
> 0K - Os dados deverão ser integrados com o serviço de métricas, caso isso não ocorra (por qualquer motivo) deverá ser feito rollback e falhar o request; <br>
> OK - A API REST deverá retornar um erro quando exceder o timeout ou a quantidade de tentativas de algum serviço dependente; <br>
> OK - cache ttl <br>
> OK - 92% (pytest) - testes unitaríos com cobertura de > 80% <br>
> OK - Tratamento de erros no acesso aos serviços externos <br>


# Explicação do projeto

## Estrutura

>src: contem todo o código do projeto <br>
>tests: contem os testes <br>
>htmlcov: resultado do pytest executado nos testes unitários (essa pasta eu só comitei para vocês verem a cobertura) <br>


###src

####app
aqui deve ficar os arquivos referentes a inicialização da aplicação
e outras configuraçãoes que poderiam estar aqui também da aplicação

####controller
como na arquitetura MVC-model,view,controler.
Faz o meio de campo entre a view a o model.
O controle de fluxo de dados.

####dao
Utilizei este padrão para desacoplar o código de banco de dados.
Assim, é possível referenciar no modelo apenas as 
operações necessárias com os dados, ao inves de acoplar
referencias de banco de dados.
Isso é bom pois caso necessite de colocar uma nova fonte
de dados ou salvar as informações em outra fonte de dados,
a manutenção fica mais fácil pois só será necessário criar uma
nova classe de DAO para outro banco e a responsabilidade
de conectar, conversar com o banco na sua linguagem
fica encapsulada nessa classe.

####services
aqui eu quis deixar os acessos a aplicações externas.
Então, cada serviço trata o acesso a uma API externa.
Mas, se tivesse que acessar alguma outra base de dados
externa para capturar dados, por exemplo, poderia ficar
nessa pasta.

####views
e aqui fica toda a parte da 'interface' da aplicação, que no 
caso da API são as rotas que o usuário consegue acessar.
#####schemas
dentro da views criei uma pasta schemas 
que tem o esqueleto das requisições.
Já usei bastante esse modelo para fazer APIs.
Eu vejo que é bom para facilitar a leitura do código
e organização.
Mas acaba dando um pouco mais de trabalho.

###tests
####unittests
pasta que contem os testes unitários da aplicação.
Aqui eu coloquei apenas um arquivo com os testes unitários das rotas.
Eu pensei eu fazer o teste usando a unidade rotas,
pois assim, se tiver alteração dentro dos models ou dos controllers,
meus testes nao são afetados.
Os testes só seriam afetados se mudasse o requisito da rota.
Basicamente fiz um teste para cada requisito incluindo
os cenários de erros nos serviços externos.

Para executar os teste com o resultado de cobertura,
basta executar:

~~~
python -m pytest --cov-report html --cov=src tests
~~~

###Como rodar
Basta baixar e ter o docker-compose instalado.
Dentro da pasta raiz, executar: <br>
~~~
docker-compose up
~~~
Ele deve subir dois containers: um do mongo e outro da aplicação.

Utilizei o python-dotenv para deixar parametrizavel
os dados de acesso ao banco de dados.
Neste caso nem precisaria, mas por costume de fazer assim eu deixei.
O acesso ao mongo fica pelo nome do container 'mongo'.
Essas informações ficam no arquivo .env.config.
Isso aqui poderia ter uma arquivo de .config para cada ambiente que
estivesse rodando a aplicação, no caso de PROD, HML.. por exemplo.


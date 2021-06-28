# Api Medical
api para obter prescrições médicas

# Requisitos

> OK - O serviço de prescrição deverá persistir no banco de dados somente os atributos recebidos no request;
> OK - Os serviços dependentes deverão ser consultados para compor os dados a serem enviados ao serviço de métricas;
> OK - Se o serviço de clínicas não responder, o request deverá seguir normalmente, pois o nome da clínica é o único atributo não obrigatório do serviço de métricas;
> 0K - Os dados deverão ser integrados com o serviço de métricas, caso isso não ocorra (por qualquer motivo) deverá ser feito rollback e falhar o request;
> OK - A API REST deverá retornar um erro quando exceder o timeout ou a quantidade de tentativas de algum serviço dependente;
> OK - cache ttl
> OK - 92% (pytest) - testes unitaríos com cobertura de > 80%
> OK - Tratamento de erros no acesso aos serviços externos
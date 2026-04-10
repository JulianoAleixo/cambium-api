# Uso de IA no desenvolvimento da API Cambium

Este documento apresenta uma análise clara e detalhada do uso de Inteligência Artificial (GitHub Copilot) durante o desenvolvimento do projeto *cambium-api*. A ideia é mostrar como a IA contribuiu ao longo do nosso processo, incluindo a arquitetura até a parte de CI/CD, destacando tanto os acertos quanto os pontos que precisaram de ajustes na prática. Inclusive para a geração desse relatório, a IA ajudou a agregar todos os passos tomados e a estruturação do presente relatório.

É válido ressaltar que em alguns momentos a IA serviu como guia, e não fez nenhum código, apenas mostrou direcionamentos, e em outros ela ajudou com a parte de codar, mas com códigos que foram constantemente validados e revisados para garantir a maior qualidade do nosso projeto. Com isso conseguimos fazer um trabalho completo, satisfatório e dentro de um tempo hábil, aplicando sempre boas práticas de Engenharia de Software e cumprindo com os requisitos que foi passado para esse trabalho.

---

## Prompts

As interações com a IA evoluíram junto com o projeto. No começo, o foco estava mais em decisões conceituais e estruturação. Com o tempo, as perguntas passaram a envolver problemas mais complexos de infraestrutura, arquitetura e integração contínua.

### Decisões Tecnológicas e Design de Software  
No início, a IA foi usada principalmente para ajudar na escolha de tecnologias e na definição da estrutura do projeto. Foram feitas perguntas como qual API de câmbio usar e como organizar os diretórios em uma aplicação com Flask.

Depois, houve pedidos mais específicos, como montar um plano para consumir a API Frankfurter e definir a melhor forma de implementar uma rota de *Health Check*. Nesse caso, a preocupação era fazer algo mais profissional, mantendo essa rota separada da lógica principal da aplicação.

### Aprendizado e Visão Crítica  
Em um certo momento, surgiu a preocupação de não transformar o projeto em um simples “repassador de dados”. Por isso, foi definida em alguns momentos que a IA não deveria entregar código pronto diretamente, mas sim ajudar como uma espécie de guia, permitindo que o desenvolvimento fosse mais ativo e focado no aprendizado.

### CI/CD e Requisitos  
A IA também foi bastante usada como apoio em DevOps. Surgiram dúvidas sobre organização de arquivos YAML, escolha de actions seguras e estruturação do pipeline.

Além disso, houve discussões sobre quando executar o job de Health Check: antes ou depois do deploy na Railway.

### Resolução de Problemas e Controle de Versão  
A IA ajudou na investigação de erros (como o `KeyError: 'rates'`), problemas de linting e dúvidas com Git. Também deu suporte em situações práticas, como recuperar branches “perdidas” por erro de digitação e atualizar um Pull Request já aberto sem precisar criar outro.

---

## Respostas da IA

A IA conseguiu entender bem o contexto do projeto e, na maioria das vezes, trouxe soluções que não só resolviam o problema, mas também melhoravam a qualidade geral do código.

### Arquitetura e Organização  
Foram sugeridas boas práticas para estruturação com Flask, incluindo organização de módulos, uso de PostgreSQL e documentação com Swagger. 
Algumas dessas práticas foram adotadas, outras não.

Um destaque foi a recomendação de usar *Flask Blueprints* para o Health Check. Isso levou à criação de um módulo separado (`health.py`), deixando o código mais limpo e organizado.

### DevOps e Estratégia de Testes  
No GitHub Actions, a IA ajudou a montar um pipeline eficiente. 

Para o deploy, foi sugerida a estratégia de “Double Health Check”:  
- um teste local antes do deploy, como segurança  
- e outro após o deploy, verificando se a aplicação está funcionando na Railway  

### Suporte no Git  
Durante o desenvolvimento, a IA atuou como guia e em certos momentos como geradora de código. O bom uso foi que, em vez de entregar respostas prontas, incentivou a análise dos problemas.

No Git, ajudou com comandos específicos para atualizar PRs e orientou como acompanhar execuções pela aba *Actions*, o que facilitou bastante o fluxo de trabalho.

### Ajustes de Infraestrutura  
Também auxiliou na formatação de arquivos Markdown e na correção de problemas com o Black que estavam quebrando o pipeline.

---

## Avaliação e Conclusões

### Precisão e Adaptação
Um ponto importante foi perceber que, apesar das respostas da IA serem tecnicamente corretas, elas quase sempre precisaram de adaptação.

Ou seja, a IA entregou uma base muito boa, mas não algo pronto para uso direto. Foi necessário ajustar algumas coisas ao contexto real do projeto.

### Pontos Fortes  
A IA agregou muito valor, com discussões sobre arquitetura e execução de tarefas repetitivas, como substituir um ponto em comum em todo o código, evitando que tívessemos que caçar linha a linha. Algumas decisões — como o uso de Blueprints e o “Double Health Check” — elevaram bastante o nível do projeto.

### Limitações  
Apesar disso, alguns problemas apareceram. Além dos citados ao longo do relatório, outros vistos foram:
- A IA sugeriu apenas tratar um erro (`try/except`) em vez de investigar a causa real

Nesse caso específico, foi necessário direcionar melhor a análise para descobrir que o problema estava na requisição HTTP.

- Blocos e trechos de código nem sempre modularizados, com trechos grandes e em um único bloco, ao invés de criar funções e módulos específicos que poderiam ser reaproveitados.

-Necessidade de mais contexto para melhores resultados

---

## Consideração Final  
Mesmo com alguns ajustes necessários, o uso da IA trouxe um ganho claro de produtividade e qualidade. Ela funcionou como um suporte constante, acelerando decisões e ajudando a manter um bom padrão técnico ao longo do projeto, e a realizar determinadas tarefas. O uso consciente é necessário e agregou bastante ao conhecimento geral do grupo. Vale lembrar que, como boa dica para prompts, é legal sempre definir o que ela deve e não deve fazer, e ser claro, dando instruções claras ("faça", "mude", "sugira", "analise").

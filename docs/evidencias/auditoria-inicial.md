# Auditoria inicial executada em 06/11/2026

Reprodução: `python scripts/auditar_historico.py <caminho-do-zip>`. Dependências locais: pandas, numpy e PyYAML. Evidências completas e hashes dos CSVs estão em auditoria-inicial.json. Nenhum dado foi alterado.

- 240.384 transações e 240.384 rótulos, sem IDs duplicados; junção 1:1 sem perdas ou sobras.
- Nenhuma violação encontrada nas verificações de nulos, categorias, finitude, inteiros, booleanos e limites das 13 features.
- Datas de transação válidas e coerentes com hora e dia da semana.
- Razão valor/média compatível com arredondamento de quatro casas: erro máximo aproximadamente 0,00005; nenhuma linha fora de tolerância absoluta de 0,000051. Isso não demonstra a disponibilidade temporal correta das médias upstream.
- Todos os rótulos são binários. data_contestacao está ausente em 236.886 registros, todos de classe 0; nenhuma fraude sem essa data. Não excluir legítimos por essa ausência. A maturidade dos lotes futuros ainda precisa ser tratada separadamente.

| Semana | Custo de aprovar tudo | Custo da regra Pix > R$ 1.000 |
|---|---|---|
| 11 | R$ 177.029,27 | R$ 102.820,44 |
| 12 | R$ 199.006,26 | R$ 122.529,35 |

Resultados preliminares: não provam ausência de vazamento na construção das features, nem confirmam a semântica de todos os cálculos históricos. Nenhum modelo treinado. Auditar intervalos temporais de rótulos, consistência das semanas e disponibilidade das features antes de declarar auditoria completa.

Estes resultados devem ser resumidos na seção 1 do notebook e copiados para a documentação exportada na entrega.

## Complemento temporal

O arquivo auditoria-temporal.json registra 200.887 linhas em treino e 39.497 em validação. As semanas são consecutivas, de 01/06/2026 a 23/08/2026, sem sobreposição dos intervalos semanais observados. Nenhuma contestação de fraude inválida ou anterior à transação; atrasos observados entre aproximadamente zero e sete dias. Isso não implica que o lote esteja completo antes do encerramento definido pelo negócio.

Há 22.674 clientes presentes em treino e validação. Repetição de cliente é compatível com prever transações futuras da base existente; não substituímos o corte temporal exigido por uma divisão por cliente. id_cliente permanece fora das features. Generalização para clientes inéditos é uma questão distinta, não demonstrada por esse resultado.

Não foram identificadas razões para excluir ou imputar linhas nas verificações executadas. A disponibilidade histórica de médias, contagens e distâncias não pode ser reconstruída apenas com este pacote: usar as features fornecidas segundo o contrato e declarar a limitação, sem afirmar ausência comprovada de vazamento upstream.

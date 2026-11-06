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

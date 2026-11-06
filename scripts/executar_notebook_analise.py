"""Executa o notebook completo no snapshot de entrega e salva inclusive falhas."""
import sys,json,shutil
from pathlib import Path
from nbclient import NotebookClient
import nbformat
from preparar_entrega_analise import preparar,ROOT


def main():
    destino=preparar()
    notebook_path=destino/"01_analise_e_escolha.ipynb"
    nb=nbformat.read(notebook_path,as_version=4)
    print("ENTREGA:",destino,flush=True)
    def progresso(cell,cell_index,**kwargs):
        if cell.cell_type=="code":print(f"Executando célula {cell_index+1}/{len(nb.cells)}",flush=True)
    try:
        NotebookClient(nb,timeout=900,kernel_name="aurora-mlops",resources={"metadata":{"path":str(destino)}},on_cell_start=progresso).execute()
    finally:
        nbformat.write(nb,notebook_path)
    codes=[c for c in nb.cells if c.cell_type=="code"]
    assert all(c.execution_count is not None for c in codes)
    assert not any(o.output_type=="error" for c in codes for o in c.outputs)
    saida=max((destino/"resultados_reproducao").iterdir())
    shutil.copy2(saida/"RESUMO_ESCOLHA.md",destino/"RESUMO_ESCOLHA.md")
    shutil.copy2(notebook_path,ROOT/"notebooks/01_analise_e_escolha.ipynb")
    verificado={"pasta":str(destino.relative_to(ROOT)),"celulas_codigo":len(codes),"todas_executadas":True,"erros":0,"resultados":str(saida.relative_to(destino))}
    (destino/"VERIFICACAO_EXECUCAO.json").write_text(json.dumps(verificado,indent=2),encoding="utf-8")
    (ROOT/"docs/evidencias/notebook-reproduzido.json").write_text(json.dumps(verificado,indent=2),encoding="utf-8")
    try:
        from nbconvert import HTMLExporter
        html,_=HTMLExporter().from_notebook_node(nb)
        (destino/"01_analise_e_escolha.html").write_text(html,encoding="utf-8")
    except ImportError:print("Prévia HTML não gerada: nbconvert indisponível.",flush=True)
    shutil.make_archive(str(destino),"zip",root_dir=destino)
    print("CONCLUÍDO:",json.dumps(verificado),flush=True)


if __name__=="__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()

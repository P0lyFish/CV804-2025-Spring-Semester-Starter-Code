OBJECT="bunny-500"
METHOD="rbf"


python main.py --input_path data/$OBJECT.pts \
               --mesh_save_path computed_meshes/$OBJECT.ply \
               --mode $METHOD \

# sphinx_liepa_train_docker

Prielaidą, kad vartoojas žino kas yra linux ir docker.

1. Parsitempti docker sphinx mokymo failus: 
   ```
   docker pull mondhs/sphinx_liepa_train
   ```
1. sukurti direktoriją */home/VARTOTOJAS/liepa_test* - vadinsim *LIEPA_DIREKTORIJA*
1. Parsisiųsti LIEPA_garsynas_1.10.zip https://drive.google.com/drive/folders/1HgWjBn7LGFueSIfQe0wN_-sxd6TOPPsI
   1. užima zip 1,3GB. Iš archivuotas 1,6GB
1. Išskleisti */home/VARTOTOJAS/liepa_test/LIEPA_garsynas*. Jame turi būti svarbiasios direktorijos:
   1. ./LIEPA_garsynas/sphinx_files/
   1. ./LIEPA_garsynas/test_repo/
   1. ./LIEPA_garsynas/train_repo/
1. Paleisti komandą su bash mokymo sąsaja *LIEPA_DIREKTORIJOJE*
   ```
   docker run  -v $(realpath ./LIEPA_garsynas):/data -it mondhs/sphinx_liepa_train bash
   ```
1. docker nueiti į ```cd /opt/sphinx_liepa_train/```
1. paleisti ```sh run.sh```
1. mkymo pabaigoje galima suspausti svarbiausias bylas su ```sh archive.sh``` ir persiųsti jas į */home/VARTOTOJAS/liepa_test/LIEPA_garsynas*

   
   

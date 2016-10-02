# tsf2csv
Convert Tagged Spot File (.tsf from MicroManager) to Comma Separated Values file(.csv for thunderSTORM)

# usage
```
python TaggedSpot2CSV.py xxx.tsf output.csv
```

# note

Only the following fields are exported:
```
frame,x [nm],y [nm],z [nm],intensity [photon]
```

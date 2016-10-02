# TaggedSpot2CSV
Convert Tagged Spot File (.tsf from MicroManager) to Comma Separated Values file(.csv for thunderSTORM)

## dependency
You need to install protobuf before use this script.

```
pip install protobuf
```

## usage
```
python TaggedSpot2CSV.py xxx.tsf output.csv
```

## note

Only the following fields are exported:
```
frame,x [nm],y [nm],z [nm],intensity [photon]
```

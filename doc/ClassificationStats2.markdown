This contains interesting statistics that we can learn by collecting some of the counters listed in `doc/ClassificationCounters.markdown`.

## Popularity of hidden service protocol

We estimate the popularity of the hidden service protocol by predicting the fraction of middle circuits that are rendezvous circuits. This is done with the following counters:

```
# estimated / predicted (the following two are complimentary)
MidNoSignalPredictRendPurposeCircuitCount / MidNoSignalPredictPurposeCircuitCount
MidNoSignalPredictNotRendPurposeCircuitCount / MidNoSignalPredictPurposeCircuitCount
```

The accuracy of the above predictions can be checked with the following:

```
# ground truth (the following two are complimentary)
MidGotSignalPredictRendPurposeCircuitCount / MidGotSignalPredictPurposeCircuitCount
MidGotSignalPredictNotRendPurposeCircuitCount / MidGotSignalPredictPurposeCircuitCount
```

These predictions can be cross-checked by counting the following:

```
# measured
TODO:?: Rend2CircuitCount / EntryCircuitCount
TODO:?: Rend2CircuitCount / EndCircuitCount
TODO:?: Rend2ClientCircuitCount / ExitAndRend2ClientCircuitCount
TODO:?: Rend2ServiceCircuitCount / ExitAndRend2ServiceCircuitCount
TODO:?: Rend2MultiHopClientCircuitCount / (MidCircuitCount / 2)
TODO:?: Rend2MultiHopServiceCircuitCount / (MidCircuitCount / 2)
```

## Liklihood of serving in CGM position

The liklihood of serving in the CGM position is predicted with the following counters:

```
# estimated / predicted (the following two are complimentary)
MidNoSignalPredictRendPurposePredictCGMPositionCircuitCount / MidNoSignalPredictRendPurposeCircuitCount
MidNoSignalPredictRendPurposePredictNotCGMPositionCircuitCount / MidNoSignalPredictRendPurposeCircuitCount
```

This can probably be computed with bandwidth weights. We also check the accuracy with the following:

```
# ground truth (the following two are complimentary)
MidGotSignalPredictRendPurposePredictCGMPositionCircuitCount / MidGotSignalPredictRendPurposeCircuitCount
MidGotSignalPredictRendPurposePredictNotCGMPositionCircuitCount / MidGotSignalPredictRendPurposeCircuitCount
```

These predictions can be cross-checked by counting the following:

```
# measured
# for rendezvous circuits, our relay should appear in the CGM position on roughly as
# many circuits as it appears in the rend position
MidNoSignalPredictRendPurposePredictCGMPositionCircuitCount == Rend2ClientCircuitCount
```

## Popularity of Facebook onion site front page

The popularity of Facebook is predicted with the following counters:

```
# estimated / predicted (the following two are complimentary)
MidNoSignalPredictRendPurposePredictCGMPositionPredictSiteCircuitCount / MidNoSignalPredictRendPurposePredictCGMPositionCircuitCount
MidNoSignalPredictRendPurposePredictCGMPositionPredictNotSiteCircuitCount / MidNoSignalPredictRendPurposePredictCGMPositionCircuitCount
```

We also check the accuracy with the following:

```
# ground truth (the following two are complimentary)
MidGotSignalPredictRendPurposePredictCGMPositionPredictSiteCircuitCount / MidGotSignalPredictRendPurposePredictCGMPositionCircuitCount
MidGotSignalPredictRendPurposePredictCGMPositionPredictNotSiteCircuitCount / MidGotSignalPredictRendPurposePredictCGMPositionCircuitCount
```

These predictions can be cross-checked by counting the following:

```
# measured
Rend2SingleOnionServiceFacebookASNCircuitCount / Rend2ServiceCircuitCount
```

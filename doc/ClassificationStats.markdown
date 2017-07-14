This contains interesting statistics that we can learn by collecting some of the counters listed in `doc/ClassificationCounters.markdown`.

## Client and Service Rendezvous

**a. Fraction of all circuits that are Rend circuits at either end**  
tag: _[RELAY]_  

```
RendCircuitCount / EntryCircuitCount
RendCircuitCount / EndCircuitCount
```

Notes:
  * Includes overhead, client + service
  * There are no equivalent classification counters that can be used to compute this statistic, because the classifier is only trained on client circuits.

## Client Rendezvous

**b. Fraction of client data circuits that are Rend client data circuits**  
tag: _[CLIENT]_  

```
RendClientCircuitCount / ExitAndRendClientCircuitCount
RendServiceCircuitCount / ExitAndRendServiceCircuitCount
```

Notes:
  * Excludes overhead, just client circuits
  * _[CLIENT]_ should be slightly greater than half _[RELAY]_, because _[RELAY]_ includes directory and preemptive circuit overheads in `EntryCircuitCount` and `EndCircuitCount`.
  * There are no equivalent classification counters that can be used to compute this statistic, because the classifier is only trained by observing client circuits from the middle position.

**c. Fraction of mid circuits that are anonymous rend client data circuits**  
tag: _[MID]_  

```
RendMultiHopClientCircuitCount / MidCircuitCount
```

Notes:
  * Measured in different positions
  * We use `RendMultiHopClientCircuitCount`, because `RendClientCircuitCount` includes Tor2web, but `MidCircuitCount` does not.
  * This is slightly inaccurate, because `MidCircuitCount` counts 4-hop circuits 2 times, 5-hop circuits 3 times,
6-hop circuits 4 times, and 7-hop circuits 5 times.

**d. Fraction of mid circuits that we know are Rend client data circuits**  
tag: _[KNOWN_MID]_  

```
MidGuessedFirstMidOnClientRendSignaledCircuitCount / MidGuessedPositionCircuitCount
```

Notes:  
  * These counters all count "client rendezvous circuit observed from the first client middle position".
So it only makes sense to collect them in middle positions.
  * _[KNOWN_MID]_ should be similar to _[MID]_, taking into account classifier accuracy and multi-middle counts in `MidGuessedPositionCircuitCount` and `MidCircuitCount`.

**e. Fraction of mid circuits that we guess are Rend client data circuits**  
tag: _[PREDICTED_MID]_  

```
MidGuessedFirstMidOnClientRendCircuitCount / MidGuessedPositionCircuitCount
```

Notes:  
  * These counters all count "client rendezvous circuit observed from the first client middle position".
So it only makes sense to collect them in middle positions.
  * _[PREDICTED_MID]_ should be similar to _[KNOWN_MID]_ and _[MID]_, taking into account classifier accuracy and
multi-middle counts in `MidGuessedPositionCircuitCount` and `MidCircuitCount`.

## Facebook Client Rendezvous

**g. Fraction of single onion services that are Facebook**  
tag: _[SINGLE_ONION_FACEBOOK]_  

```
RendSingleOnionServiceFacebookASNCircuitCount / RendSingleOnionServiceCircuitCount
```

Notes:  
  * There are no equivalent classification counters for these circuits, because the classifier is only trained by observing client circuits: it can't tell if they are single onion services on the other end.

**h. Fraction of all onion services that are Facebook**  
tag: _[FACEBOOK]_  

```
RendSingleOnionServiceFacebookASNCircuitCount / RendServiceCircuitCount
```

**i. Fraction of mid circuits that we know are Facebook Rend client data circuits**  
tag: _[KNOWN_FACEBOOK]_  

```
MidGuessedFacebookFirstMidOnClientRendSignaledCircuitCount / MidGuessedSitePositionCircuitCount
```

Notes:  
  * These counters all count "facebook client rendezvous circuit observed from the first client middle position".
So it only makes sense to collect them in middle positions.
  * _[KNOWN_FACEBOOK]_ should be similar to _[FACEBOOK]_, taking into account classifier accuracy and multi-middle counts in `MidGuessedSitePositionCircuitCount` (but not in `RendServiceCircuitCount`).

**j. Fraction of mid circuits that we guess are Facebook Rend client data circuits**  
tag: _[PREDICTED_FACEBOOK]_  

```
MidGuessedFacebookFirstMidOnClientRendCircuitCount / MidGuessedSitePositionCircuitCount
```

Notes:  
  * These counters all count "client rendezvous circuit observed from the first client middle position".
So it only makes sense to collect them in middle positions.
  * _[PREDICTED_FACEBOOK]_ should be similar to _[KNOWN_FACEBOOK]_ and _[FACEBOOK]_, taking into account classifier accuracy and multi-middle counts in `MidGuessedSitePositionCircuitCount` (but not in `RendServiceCircuitCount`).

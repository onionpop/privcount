## Client and Service Rendezvous

**a. Fraction of all circuits that are Rend circuits at either end**  
tag: _[RELAY]_  
notes: includes overhead, client + service  

```
RendCircuitCount / EntryCircuitCount
RendCircuitCount / EndCircuitCount
```

where:  
`RendCircuitCount`: circuits observed in the rendezvous position, client or service side  
`EntryCircuitCount`: circuits observed in the entry position (includes client, service, exit, and overheads)  
`EndCircuitCount`: circuits observed in the entry position (includes client, service, exit, and overheads)  

There are no equivalent "Guessed" counters for these circuits, because the classifier is only trained on client circuits.

## Client Rendezvous

**b. Fraction of client data circuits that are Rend client data circuits**  
tag: _[CLIENT]_  
notes: excludes overhead, just client  

```
RendClientCircuitCount / ExitAndRendClientCircuitCount
RendServiceCircuitCount / ExitAndRendServiceCircuitCount
```

where:  
`RendServiceCircuitCount`: circuits observed in the rendezvous position, service side  
`RendClientCircuitCount`: circuits observed in the rendezvous position, client side (includes circuits where the service never connected)  
`ExitCircuitCount`: circuits observed in the exit position (client exit data circuits)  

and so that we don't add two lots of noise, these sums will be stored in their own counters:

```
ExitAndRendClientCircuitCount` = (ExitCircuitCount + RendClientCircuitCount)
ExitAndRendServiceCircuitCount = (ExitCircuitCount + RendServiceCircuitCount)
```

_[CLIENT]_ should be slightly greater than half _[RELAY]_, because _[RELAY]_ includes directory and preemptive circuit overheads in `EntryCircuitCount` and `EndCircuitCount`.

There are no equivalent "Guessed" counters for these circuits, because the classifier is only trained by observing client circuits from the middle position.

**c. Fraction of mid circuits that are anonymous rend client data circuits**  
tag: _[MID]_  
notes: measured in different positions  

```
RendMultiHopClientCircuitCount / MidCircuitCount
```

where:  
`RendMultiHopClientCircuitCount`: circuits observed in the rendezvous position, client side, multi-hop circuit
(excludes Tor2web)  
`MidCircuitCount`: circuits observed in a middle position (multiple counts on multi-middle circuits)  

We use `RendMultiHopClientCircuitCount`, because `RendClientCircuitCount` includes Tor2web, but `MidCircuitCount` does not.

This is slightly inaccurate, because `MidCircuitCount` counts 4-hop circuits 2 times, 5-hop circuits 3 times,
6-hop circuits 4 times, and 7-hop circuits 5 times.

**d. Fraction of mid circuits that we know are Rend client data circuits**  
tag: _[KNOWN_MID]_  

```
MidGuessedFirstMidOnClientRendSignaledCircuitCount / MidGuessedPositionCircuitCount
```

where:  
`MidGuessedFirstMidOnClientRendSignaledCircuitCount`: circuit was signaled, we guessed position right  
`MidGuessedNotFirstMidOnClientRendSignaledCircuitCount`: circuit was signaled, we guessed position wrong  
`MidGuessedFirstMidOnClientRendNotSignaledCircuitCount`: circuit was not signaled, we guessed position wrong  
`MidGuessedNotFirstMidOnClientRendNotSignaledCircuitCount`: circuit was not signaled, we guessed position right  
`MidGuessedPositionCircuitCount`: total number of circuits which were analysed by the position classifier  

These counters all count "client rendezvous circuit observed from the first client middle position".
So it only makes sense to collect them in middle positions.

_[KNOWN_MID]_ should be similar to _[MID]_, taking into account classifier accuracy and multi-middle counts in `MidGuessedPositionCircuitCount` and `MidCircuitCount`.

**e. Fraction of mid circuits that we guess are Rend client data circuits**  
tag: _[GUESSED_MID]_  

```
MidGuessedFirstMidOnClientRendCircuitCount / MidGuessedPositionCircuitCount
```

where:  
`MidGuessedFirstMidOnClientRendCircuitCount`: we guessed the position we want  
`MidGuessedNotFirstMidOnClientRendCircuitCount`: we guessed a position we don't want  

These counters all count "client rendezvous circuit observed from the first client middle position".
So it only makes sense to collect them in middle positions.

_[GUESSED_MID]_ should be similar to _[KNOWN_MID]_ and _[MID]_, taking into account classifier accuracy and
multi-middle counts in `MidGuessedPositionCircuitCount` and `MidCircuitCount`.

## Facebook Client Rendezvous

**f. Fraction of rend service circuits that are single onion**  
tag: _[SINGLE_ONION]_  

```
RendSingleOnionServiceCircuitCount / RendServiceCircuitCount
```

where:  
`RendSingleOnionServiceCircuitCount`: circuits observed in the rendezvous position, service side, single hop

This counter is interesting, but unrelated to the guesses we are making.

**g. Fraction of single onion services that are Facebook**  
tag: _[SINGLE_ONION_FACEBOOK]_  

```
RendSingleOnionServiceFacebookASNCircuitCount / RendSingleOnionServiceCircuitCount
```

where:  
`RendSingleOnionServiceFacebookASNCircuitCount`: circuits observed in the rendezvous position, service side, single hop, service IP address is in a Facebook ASN

There are no equivalent "Guessed" counters for these circuits, because the classifier is only trained by observing client circuits: it can't tell if they are single onion services on the other end.

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

where:  
`MidGuessedFacebookFirstMidOnClientRendSignaledCircuitCount`: circuit was signaled, we guessed position and site right  
`MidGuessedNotFacebookFirstMidOnClientRendSignaledCircuitCount`: circuit was signaled, we guessed position right but site wrong  
`MidGuessedFacebookFirstMidOnClientRendNotSignaledCircuitCount`: circuit was not signaled, we guessed position and site wrong  
`MidGuessedNotFacebookFirstMidOnClientRendNotSignaledCircuitCount`: circuit was not signaled, we guessed position wrong but site right  
`MidGuessedSitePositionCircuitCount`: total number of circuits which were analysed by the site classifier (and the position classifier)  

These counters all count "facebook client rendezvous circuit observed from the first client middle position".
So it only makes sense to collect them in middle positions.

_[KNOWN_FACEBOOK]_ should be similar to _[FACEBOOK]_, taking into account classifier accuracy and multi-middle counts in `MidGuessedSitePositionCircuitCount` (but not in `RendServiceCircuitCount`).

**j. Fraction of mid circuits that we guess are Facebook Rend client data circuits**  
tag: _[GUESSED_FACEBOOK]_  

```
MidGuessedFacebookFirstMidOnClientRendCircuitCount / MidGuessedSitePositionCircuitCount
```

where:  
`MidGuessedFacebookFirstMidOnClientRendCircuitCount`: we guessed the site we want  
`MidGuessedNotFacebookFirstMidOnClientRendCircuitCount`: we guessed a site we don't want  

These counters all count "client rendezvous circuit observed from the first client middle position".
So it only makes sense to collect them in middle positions.

_[GUESSED_FACEBOOK]_ should be similar to _[KNOWN_FACEBOOK]_ and _[FACEBOOK]_, taking into account classifier accuracy and multi-middle counts in `MidGuessedSitePositionCircuitCount` (but not in `RendServiceCircuitCount`).

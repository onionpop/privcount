The following is the list of counters that we can count to learn the statistics listed in `doc/ClassificationStats.markdown`.

`Rend2CircuitCount`: circuits observed in the rendezvous position, client or service side  
`EntryCircuitCount`: circuits observed in the entry position (includes client, service, exit, and overheads)  
`EndCircuitCount`: circuits observed in the end position (includes client, service, exit, and overheads)  

`Rend2ServiceCircuitCount`: circuits observed in the rendezvous position, service side  
`Rend2ClientCircuitCount`: circuits observed in the rendezvous position, client side (includes circuits where the service never connected)  
`ExitCircuitCount`: circuits observed in the exit position (client exit data circuits)  
`ExitAndRend2ClientCircuitCount`: sum of (ExitCircuitCount + RendClientCircuitCount) with a single lot of noise  
`ExitAndRend2ServiceCircuitCount`: sum of (ExitCircuitCount + RendServiceCircuitCount) with a single lot of noise  

`Rend2MultiHopClientCircuitCount`: circuits observed in the rendezvous position, client side, multi-hop circuit
(excludes Tor2web)  
`MidCircuitCount`: circuits observed in a middle position (multiple counts on multi-middle circuits)  

`Rend2SingleOnionServiceCircuitCount`: circuits observed in the rendezvous position, service side, single hop  
`Rend2SingleOnionServiceFacebookASNCircuitCount`: circuits observed in the rendezvous position, service side, single hop, service IP address is in a Facebook ASN  

---

Counters for classification, these are implemented in data_collector.py. These are all middle circuits.

Total:

`MidPredictPurposeCircuitCount`: total number of circuits passed to the purpose predictor
`MidGotSignalPredictPurposeCircuitCount`: of above, the number of circuits that we originated at our crawler
`MidNoSignalPredictPurposeCircuitCount`: of above, the number that we did not originate

Rendezvous:

`MidPredictRendPurposeCircuitCount`: total number of circuits that we predicted are rendezvous
`MidGotSignalPredictRendPurposeCircuitCount`: of above, originated at our crawler
`MidNoSignalPredictRendPurposeCircuitCount`: of above, did not originate at our crawler

`MidPredictNotRendPurposeCircuitCount`: total number of circuits that we predicted are NOT rendezvous
`MidGotSignalPredictNotRendPurposeCircuitCount`: of above, originated at our crawler
`MidNoSignalPredictNotRendPurposeCircuitCount`: of above, did not originate at our crawler

Rendezvous, CGM:

`MidPredictRendPurposePredictCGMPositionCircuitCount`: total number of predicted rendezvous circuits that we predicted we are in the CGM position
`MidGotSignalPredictRendPurposePredictCGMPositionCircuitCount`: of above, originated at our crawler
`MidNoSignalPredictRendPurposePredictCGMPositionCircuitCount`: of above, did not originate at our crawler

`MidPredictRendPurposePredictNotCGMPositionCircuitCount`: total number of predicted rendezvous circuits that we predicted we are NOT in the CGM position
`MidGotSignalPredictRendPurposePredictNotCGMPositionCircuitCount`: of above, originated at our crawler
`MidNoSignalPredictRendPurposePredictNotCGMPositionCircuitCount`: of above, did not originate at our crawler

Rendezvous, CGM, Facebook:

`MidPredictRendPurposePredictCGMPositionPredictSiteCircuitCount`: total number of predicted rendezvous, predicted CGM circuits that we predict are Facebook circuits
`MidGotSignalPredictRendPurposePredictCGMPositionPredictSiteCircuitCount`: of above, originated at our crawler
`MidNoSignalPredictRendPurposePredictCGMPositionPredictSiteCircuitCount`: of above, did not originate at our crawler

`MidPredictRendPurposePredictCGMPositionPredictNotSiteCircuitCount`: total number of predicted rendezvous, predicted CGM circuits that we predict are NOT Facebook circuits
`MidGotSignalPredictRendPurposePredictCGMPositionPredictNotSiteCircuitCount`: of above, originated at our crawler
`MidNoSignalPredictRendPurposePredictCGMPositionPredictNotSiteCircuitCount`: of above, did not originate at our crawler

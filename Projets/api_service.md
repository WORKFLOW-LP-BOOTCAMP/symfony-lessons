# API Service mise à jour des crypto

```txt
my_crypto_app/
│
├── config/
│   └── service.yaml
│
├── src/

 ...

│   │
│   ├── Entity/
│   │   └── Crypto.php
│   │
│   ├── Service/
│   │   └── CryptoApiService.php  <-- dépendance : CryptoRepository et API
│   │
│   └── Repository/
│       └── CryptoRepository.php
│

...

│
└── tests/
     └── CryptoApiServiceTest.php

.env  <-- se connecter à l'API
```

Faire un diagramme de séquence pour expliciter le fonctionnement de ce service.

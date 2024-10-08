deployments = {
    # Ethereum
    "ethereum:mainnet": {
        "math": "0xc9CBC565A9F4120a2740ec6f64CC24AeB2bB3E5E",
        # "views_old_0": "0xe0B15824862f3222fdFeD99FeBD0f7e0EC26E1FA",
        # "views_old_1": "0x13526206545e2DC7CcfBaF28dC88F440ce7AD3e0",
        "views": "0xFF53042865dF617de4bB871bD0988E7B93439cCF",
        "plain_amm": "0xDCc91f930b42619377C200BA05b7513f2958b202",
        "meta_amm": "0xede71F77d7c900dCA5892720E76316C6E575F0F7",
        "factory": "0x6A8cbed756804B16E05E741eDaBd5cB544AE21bf",
        "gauge": "0x38D9BdA812da2C68dFC6aDE85A7F7a54E77F8325",
        "zap": "0xDfeF1725Ab767f165171709C6d1E1A6247425fE0",
    },
    "ethereum:sepolia": {
        "math": "0x2cad7b3e78e10bcbf2cc443ddd69ca8bcc09a758",
        # "views": "0x9d3975070768580f755D405527862ee126d0eA08",
        "views": "",
        "plain_amm": "0xE12374F193f91f71CE40D53E0db102eBaA9098D5",
        "meta_amm": "0xB00E89EaBD59cD3254c88E390103Cf17E914f678",
        "factory": "0xfb37b8D939FFa77114005e61CFc2e543d6F49A81",
        "zap": "",
    },
    # Layer 2
    "arbitrum:mainnet": {
        "math": "0xD4a8bd4d59d65869E99f20b642023a5015619B34",
        # "views_old_0": "0x9293f068912bae932843a1bA01806c54f416019D",
        # "views_old_1": "0xDD7EBB1C49780519dD9755B8B1A23a6f42CE099E",
        "views": "",
        "plain_amm": "0xf6841C27fe35ED7069189aFD5b81513578AFD7FF",
        "meta_amm": "0xFf02cBD91F57A778Bab7218DA562594a680B8B61",
        "factory": "0x9AF14D26075f142eb3F292D5065EB3faa646167b",
        "zap": "0x59AfCD3e931018dc493AA1d833B11bb5A0744906",
    },
    "optimism:mainnet": {
        "math": "0xa7b9d886A9a374A1C86DC52d2BA585c5CDFdac26",
        # "views_old_0": "0xf3A6aa40cf048a3960E9664847E9a7be025a390a",
        # "views_old_1": "0xf6841C27fe35ED7069189aFD5b81513578AFD7FF",
        "views": "0xbC7654d2DD901AaAa3BE4Cb5Bc0f10dEA9f96443",
        "plain_amm": "0x635742dCC8313DCf8c904206037d962c042EAfBd",
        "meta_amm": "0x5702BDB1Ec244704E3cBBaAE11a0275aE5b07499",
        "factory": "0x5eeE3091f747E60a045a2E715a4c71e600e31F6E",
        "zap": "0x07920E98a66e462C2Aa4c8fa6200bc68CA161ea0",
    },
    "base:mainnet": {
        "math": "0xe265FC390E9129b7E337Da23cD42E00C34Da2CE3",
        # "views_old_0": "0xa7b9d886A9a374A1C86DC52d2BA585c5CDFdac26",
        # "views_old_1": "0xC1b393EfEF38140662b91441C6710Aa704973228",
        "views": "0xA54f3c1DFa5f7DbF2564829d14b3B74a65d26Ae2",
        "plain_amm": "0xf3A6aa40cf048a3960E9664847E9a7be025a390a",
        "meta_amm": "0x635742dCC8313DCf8c904206037d962c042EAfBd",
        "factory": "0xd2002373543Ce3527023C75e7518C274A51ce712",
        "zap": "0x3f445D38E820c010a7A6E33c5F80cBEBE6930f61",
    },
    "linea:mainnet": {
        "math": "0xbC0797015fcFc47d9C1856639CaE50D0e69FbEE8",
        # "views_old_0": "0xe265FC390E9129b7E337Da23cD42E00C34Da2CE3",
        # "views_old_1": "0x3E3B5F27bbf5CC967E074b70E9f4046e31663181",
        "views": "0xB6845b562F01eB02ef20CBB63553d2a768e5a1Cb",
        "plain_amm": "0xa7b9d886a9a374a1c86dc52d2ba585c5cdfdac26",
        "meta_amm": "0xf3a6aa40cf048a3960e9664847e9a7be025a390a",
        "factory": "0x5eeE3091f747E60a045a2E715a4c71e600e31F6E",
        "zap": "0xf2eff2Cd0d9C82b7b2f17FbBed703fA7931dB1da",
    },
    "scroll:mainnet": {
        "math": "0xbC0797015fcFc47d9C1856639CaE50D0e69FbEE8",
        # "views_old_0": "0xe265FC390E9129b7E337Da23cD42E00C34Da2CE3",
        # "views_old_1": "0x20D1c021525C85D9617Ccc64D8f547d5f730118A",
        "views": "0x3f445D38E820c010a7A6E33c5F80cBEBE6930f61",
        "plain_amm": "0xa7b9d886A9a374A1C86DC52d2BA585c5CDFdac26",
        "meta_amm": "0xf3A6aa40cf048a3960E9664847E9a7be025a390a",
        "factory": "0x5eeE3091f747E60a045a2E715a4c71e600e31F6E",
        "zap": "0xb47988aD49DCE8D909c6f9Cf7B26caF04e1445c8",
    },
    "polygon-zkevm:mainnet": {
        "math": "0xe265FC390E9129b7E337Da23cD42E00C34Da2CE3",
        # "views_old_1": "0x87DD13Dd25a1DBde0E1EdcF5B8Fa6cfff7eABCaD",
        "views": "0xB6845b562F01eB02ef20CBB63553d2a768e5a1Cb",
        "plain_amm": "0xf3A6aa40cf048a3960E9664847E9a7be025a390a",
        "meta_amm": "0x635742dCC8313DCf8c904206037d962c042EAfBd",
        "factory": "0xd2002373543Ce3527023C75e7518C274A51ce712",
        "zap": "0xf2eff2Cd0d9C82b7b2f17FbBed703fA7931dB1da",
    },
    # Layer 1
    "gnosis:mainnet": {
        "math": "0xFAbC421e3368D158d802684A217a83c083c94CeB",
        # "views_old_0": "0x0c59d36b23f809f8b6C7cb4c8C590a0AC103baEf",
        # "views_old_1": "0x33e72383472f77B0C6d8F791D1613C75aE2C5915",
        "views": "0xa0EC67a3C483674f77915893346A8CA3AbE2b785",
        "plain_amm": "0x3d6cb2f6dcf47cdd9c13e4e3beae9af041d8796a",
        "meta_amm": "0xC1b393EfEF38140662b91441C6710Aa704973228",
        "factory": "0xbC0797015fcFc47d9C1856639CaE50D0e69FbEE8",
        "zap": "0x08390C76DFDaB74249754C8e71cC2747351bd388",
    },
    "polygon:mainnet": {
        "math": "0xd7E72f3615aa65b92A4DBdC211E296a35512988B",
        # "views_old_0": "0xbC0797015fcFc47d9C1856639CaE50D0e69FbEE8",
        # "views_old_1": "0x20D1c021525C85D9617Ccc64D8f547d5f730118A",
        "views": "0xf2eff2Cd0d9C82b7b2f17FbBed703fA7931dB1da",
        "plain_amm": "0xe265FC390E9129b7E337Da23cD42E00C34Da2CE3",
        "meta_amm": "0xa7b9d886A9a374A1C86DC52d2BA585c5CDFdac26",
        "factory": "0x1764ee18e8B3ccA4787249Ceb249356192594585",
        "zap": "0x4c7a5a5d57f98d362f1c00d7135f0da5b6f82227",
    },
    "avalanche:mainnet": {
        "math": "0xd7E72f3615aa65b92A4DBdC211E296a35512988B",
        # "views_old_0": "0xbC0797015fcFc47d9C1856639CaE50D0e69FbEE8",
        # "views_old_1": "0x8F7632122125699da7E22d465fa16EdE4f687Fa4",
        "views": "0xe548590f9fAe7a23EA6501b144B0D58b74Fc4B53",
        "plain_amm": "0xe265FC390E9129b7E337Da23cD42E00C34Da2CE3",
        "meta_amm": "0xa7b9d886A9a374A1C86DC52d2BA585c5CDFdac26",
        "factory": "0x1764ee18e8B3ccA4787249Ceb249356192594585",
        "zap": "0xA54f3c1DFa5f7DbF2564829d14b3B74a65d26Ae2",
    },
    "fantom:mainnet": {
        "math": "0xf3A6aa40cf048a3960E9664847E9a7be025a390a",
        # "views_old_0": "0x635742dCC8313DCf8c904206037d962c042EAfBd",
        # "views_old_1": "0x6A8cbed756804B16E05E741eDaBd5cB544AE21bf",
        "views": "0x33e72383472f77B0C6d8F791D1613C75aE2C5915",
        "plain_amm": "0x5702BDB1Ec244704E3cBBaAE11a0275aE5b07499",
        "meta_amm": "0x046207cB759F527b6c10C2D61DBaca45513685CC",
        "factory": "0xe61Fb97Ef6eBFBa12B36Ffd7be785c1F5A2DE66b",
        "zap": "0x21688e843a99B0a47E750e7dDD2b5dAFd9269d30",
    },
    "bsc:mainnet": {
        "math": "0x166c4084Ad2434E8F2425C64dabFE6875A0D45c5",
        # "views_old_0": "0x5Ea9DD3b6f042A34Df818C6c1324BC5A7c61427a",
        # "views_old_1": "0xFf02cBD91F57A778Bab7218DA562594a680B8B61",
        "views": "0xbC7654d2DD901AaAa3BE4Cb5Bc0f10dEA9f96443",
        "plain_amm": "0x505d666E4DD174DcDD7FA090ed95554486d2Be44",
        "meta_amm": "0x5a8C93EE12a8Df4455BA111647AdA41f29D5CfcC",
        "factory": "0xd7E72f3615aa65b92A4DBdC211E296a35512988B",
        "zap": "0x07920e98a66e462c2aa4c8fa6200bc68ca161ea0",
    },
    "celo:mainnet": {
        "math": "0xd7E72f3615aa65b92A4DBdC211E296a35512988B",
        # "views_old_0": "0xbC0797015fcFc47d9C1856639CaE50D0e69FbEE8",
        # "views_old_1": "0x8F7632122125699da7E22d465fa16EdE4f687Fa4",
        "views": "0xA54f3c1DFa5f7DbF2564829d14b3B74a65d26Ae2",
        "plain_amm": "0xe265FC390E9129b7E337Da23cD42E00C34Da2CE3",
        "meta_amm": "0xa7b9d886A9a374A1C86DC52d2BA585c5CDFdac26",
        "factory": "0x1764ee18e8B3ccA4787249Ceb249356192594585",
        "zap": "0x3f445D38E820c010a7A6E33c5F80cBEBE6930f61",
    },
    "kava:mainnet": {
        "math": "0xd7E72f3615aa65b92A4DBdC211E296a35512988B",
        # "views_old_0": "0xbC0797015fcFc47d9C1856639CaE50D0e69FbEE8",
        # "views_old_1": "0x20D1c021525C85D9617Ccc64D8f547d5f730118A",
        "views": "0xB6845b562F01eB02ef20CBB63553d2a768e5a1Cb",
        "plain_amm": "0xe265FC390E9129b7E337Da23cD42E00C34Da2CE3",
        "meta_amm": "0xa7b9d886A9a374A1C86DC52d2BA585c5CDFdac26",
        "factory": "0x1764ee18e8B3ccA4787249Ceb249356192594585",
        "zap": "0xf2eff2Cd0d9C82b7b2f17FbBed703fA7931dB1da",
    },
    "aurora:mainnet": {
        "math": "0xbC0797015fcFc47d9C1856639CaE50D0e69FbEE8",
        # "views_old_0": "0xe265FC390E9129b7E337Da23cD42E00C34Da2CE3",
        # "views_old_1": "0x20D1c021525C85D9617Ccc64D8f547d5f730118A",
        "views": "0xD4a8bd4d59d65869E99f20b642023a5015619B34",
        "plain_amm": "0xa7b9d886A9a374A1C86DC52d2BA585c5CDFdac26",
        "meta_amm": "0xf3A6aa40cf048a3960E9664847E9a7be025a390a",
        "factory": "0x5eeE3091f747E60a045a2E715a4c71e600e31F6E",
        "zap": "0x9293f068912bae932843a1bA01806c54f416019D",
    },
    "fraxtal:mainnet": {
        "math": "0x506F594ceb4E33F5161139bAe3Ee911014df9f7f",
        # "views_old_0": "0x87FE17697D0f14A222e8bEf386a0860eCffDD617",
        # "views_old_1": "0xFAbC421e3368D158d802684A217a83c083c94CeB",
        "views": "0xeEcCd039d7228530D5F0c3ce7291Dd9677CCFFb1",
        "plain_amm": "0x1764ee18e8B3ccA4787249Ceb249356192594585",
        "meta_amm": "0x5eeE3091f747E60a045a2E715a4c71e600e31F6E",
        "factory": "0xd2002373543Ce3527023C75e7518C274A51ce712",
        "zap": "0xe61Fb97Ef6eBFBa12B36Ffd7be785c1F5A2DE66b",
    },
    "mantle:mainnet": {
        "math": "0x8b3EFBEfa6eD222077455d6f0DCdA3bF4f3F57A6",
        # "views_old_0": "0x506F594ceb4E33F5161139bAe3Ee911014df9f7f",
        # "views_old_1": "0x166c4084Ad2434E8F2425C64dabFE6875A0D45c5",
        "views": "0xFf02cBD91F57A778Bab7218DA562594a680B8B61",
        "plain_amm": "0x87FE17697D0f14A222e8bEf386a0860eCffDD617",
        "meta_amm": "0x1764ee18e8B3ccA4787249Ceb249356192594585",
        "factory": "0x5eeE3091f747E60a045a2E715a4c71e600e31F6E",
        "zap": "0xe548590f9fAe7a23EA6501b144B0D58b74Fc4B53",
        "factory_ctor": "000000000000000000000000f3a431008396df8a8b2df492c913706bdb0874ef0000000000000000000000002d12d0907a388811e3aa855a550f959501d303ee",  # noqa:E501
    },
    "xlayer:mainnet": {
        "math": "0x8b3EFBEfa6eD222077455d6f0DCdA3bF4f3F57A6",
        # "views_old_1": "0xd7E72f3615aa65b92A4DBdC211E296a35512988B",
        "views": "0xb47988aD49DCE8D909c6f9Cf7B26caF04e1445c8",
        "plain_amm": "0x87FE17697D0f14A222e8bEf386a0860eCffDD617",
        "meta_amm": "0x1764ee18e8B3ccA4787249Ceb249356192594585",
        "factory": "0x5eeE3091f747E60a045a2E715a4c71e600e31F6E",
        "zap": "0x604388Bb1159AFd21eB5191cE22b4DeCdEE2Ae22",
    },
    "zksync:mainnet": {
        # old zkvyper:
        # "math": "0xcf19236e85000901dE2Fad3199aA4A1F74a78B6C",
        # # "views_old_1": "0xDD82bEe76CB4b161B44533e4B6Dfc2eee7e066D4",
        # "views": "0xeF62cD5CBa8B040827B648dBc6a755ddeeb84E65",
        # "plain_amm": "0x3ce3009F8ad07161BA9d02d7A0173180d0281cA4",
        # "meta_amm": "0x1E9A82C2a3DF2E0793a2B828aA652Db192f3C8F3",
        # "factory": "0x375444aeDEb6C3db897f293E1DBa85D7422A6859",
        # "zap": "0x4232Dcc6D31543A2431079BdE2082C69eA3A771E",
        # new zkvyper:
        "math": "0x29Fc22c7fEC8748a85852E2D36728D9194DDb854",
        "views": "0x59557D68d46e8367Fb357F2E848D8506cBf371c9",
        "plain_amm": "0x04D0095a1A4Ae881a078ae61F36945E85464e6d7",
        "meta_amm": "0xC5d5402481aefec461Ab86b1051AC26dF05BeE3B",
        "factory": "0xFcAb5d04e8e031334D5e8D2C166B08daB0BE6CaE",
        "zap": "0x1F280a5CFd3220b95819674a635B0D12a32F0E6a",
    },
}

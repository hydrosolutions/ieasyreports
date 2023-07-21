class Site:
    def __init__(self, site_id: int, name: str, site_code: str, region: str, basin: str):
        self.id = site_id
        self.name = name
        self.site_code = site_code
        self.site_region = region
        self.site_basin = basin

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


SITES = [
    Site(1, "Zagreb Jadranski most", "10000", "Grad Zagreb", "Sava"),
    Site(2, "Zagreb Domovinski most", "10010", "Grad Zagreb", "Sava"),
    Site(3, "Slavonski Brod", "35000", "Brodsko-posavska", "Sava"),
    Site(4, "Osijek Donji Grad", "31000", "Osjecko-baranjska", "Drava"),
    Site(5, "Vinkovci", "32100", "Vukovarsko-srijemska", "Bosut"),
    Site(6, "Vukovar Luka", "32000", "Vukovarsko-srijemska", "Dunav"),
    Site(7, "Borovo", "32227", "Vukovarsko-srijemska", "Dunav"),
    Site(8, "Donji Miholjac", "31540", "Osjecko-baranjska", "Drava"),
    Site(9, "Rugvica", "10372", "Zagrebacka", "Sava")
]

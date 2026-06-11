class RegSO:
    def __init__(
        self,
        not_on_land: bool,
        offshore: bool = False,
        objektidentitet: str | None = None,
        objekttyp: str | None = None,
        regsokod: str | None = None,
        regsonamn: str | None = None,
        lanskod: str | None = None,
        lansnamn: str | None = None,
        kommunkod: str | None = None,
        kommunnamn: str | None = None,
        version: str | None = None,
        ansvarig_organisation: str | None = None,
        referensdatum: str | None = None,
    ) -> None:
        self.not_on_land = not_on_land
        self.offshore = offshore
        self.objektidentitet = objektidentitet
        self.objekttyp = objekttyp
        self.regsokod = regsokod
        self.regsonamn = regsonamn
        self.lanskod = lanskod
        self.lansnamn = lansnamn
        self.kommunkod = kommunkod
        self.kommunnamn = kommunnamn
        self.version = version
        self.ansvarig_organisation = ansvarig_organisation
        self.referensdatum = referensdatum

    def __repr__(self) -> str:
        return (
            f"RegSO(regsokod={self.regsokod!r}, regsonamn={self.regsonamn!r}, "
            f"kommunkod={self.kommunkod!r}, kommunnamn={self.kommunnamn!r}, "
            f"lansnamn={self.lansnamn!r}, not_on_land={self.not_on_land}, "
            f"offshore={self.offshore})"
        )

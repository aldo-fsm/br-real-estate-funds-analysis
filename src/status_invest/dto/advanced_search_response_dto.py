class AdvancedSearchResponseDto:
    def __init__(self, data: dict):
        self.list = [AdvancedSearchResponseItemDto(item) for item in data['list']]
        self.totalResults: int = data['totalResults']
        self.hasForecast: bool = data['hasForecast']

class AdvancedSearchResponseItemDto:
    def __init__(self, data: dict):
        self.ticker: str = data['ticker']
        self.companyid: int = data.get('companyid')
        self.companyname: str = data.get('companyname')
        self.price: float = data.get('price')
        self.sectorid: int = data.get('sectorid')
        self.sectorname: str = data.get('sectorname')
        self.subsectorid: int = data.get('subsectorid')
        self.subsectorname: str = data.get('subsectorname')
        self.segment: str = data.get('segment')
        self.segmentid: int = data.get('segmentid')
        self.gestao: int = data.get('gestao')
        self.gestao_f: str = data.get('gestao_f')
        self.dy: float = data.get('dy')
        self.p_vp: float = data.get('p_vp')
        self.valorpatrimonialcota: float = data.get('valorpatrimonialcota')
        self.liquidezmediadiaria: float = data.get('liquidezmediadiaria')
        self.percentualcaixa: float = data.get('percentualcaixa')
        self.dividend_cagr: float = data.get('dividend_cagr')
        self.cota_cagr: float = data.get('cota_cagr')
        self.numerocotistas: int = data.get('numerocotistas')
        self.numerocotas: int = data.get('numerocotas')
        self.patrimonio: float = data.get('patrimonio')
        self.lastdividend: float = data.get('lastdividend')

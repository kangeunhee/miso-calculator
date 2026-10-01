export interface LottoStore {
  id: number;
  name: string;
  lat: number;
  lng: number;
  address: string;
  firstWinCount: number;  // 1등 당첨 횟수
  secondWinCount: number; // 2등 당첨 횟수
}

export const lottoStores: LottoStore[] = [
  {
    id: 1,
    name: "스파 (노원구)",
    lat: 37.6582,
    lng: 127.0628,
    address: "서울 노원구 동일로 1493 상계주공아파트 10단지 주공상가",
    firstWinCount: 52,
    secondWinCount: 200,
  },
  {
    id: 2,
    name: "부일카서비스 (부산 동구)",
    lat: 35.1278,
    lng: 129.0435,
    address: "부산 동구 자성로133번길 35",
    firstWinCount: 48,
    secondWinCount: 170,
  },
  {
    id: 3,
    name: "로또명당 가판점 (중구)",
    lat: 37.5665,
    lng: 126.9780,
    address: "서울 중구 태평로1가 31-25",
    firstWinCount: 30,
    secondWinCount: 95,
  },
  {
    id: 4,
    name: "강남 365 복권방",
    lat: 37.4979,
    lng: 127.0276,
    address: "서울 강남구 테헤란로 123",
    firstWinCount: 12,
    secondWinCount: 45,
  },
];
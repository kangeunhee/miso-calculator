export interface LottoStore {
  id: number;
  name: string;
  address: string;
  lat: number;
  lng: number;
  firstWinCount: number; // 1등 당첨 횟수
}

export const LOTTO_STORES: LottoStore[] = [
  {
    id: 1,
    name: "스파",
    address: "서울 노원구 동일로 1493 상계주공아파트 10단지 주공공간",
    lat: 37.6583,
    lng: 127.0628,
    firstWinCount: 48,
  },
  {
    id: 2,
    name: "부일카서비스",
    address: "부산 동구 자성로133번길 35",
    lat: 35.1531,
    lng: 129.0594,
    firstWinCount: 40,
  },
  {
    id: 3,
    name: "라이프복권방",
    address: "인천 중구 연안부두로 53",
    lat: 37.4589,
    lng: 126.6025,
    firstWinCount: 28,
  },
  {
    id: 4,
    name: "로또명당인주점",
    address: "충남 아산시 인주면 서해로 3856",
    lat: 36.8831,
    lng: 126.8883,
    firstWinCount: 26,
  },
  {
    id: 5,
    name: "복권명당",
    address: "대구 수성구 천을로 180",
    lat: 35.8456,
    lng: 128.6811,
    firstWinCount: 22,
  },
];
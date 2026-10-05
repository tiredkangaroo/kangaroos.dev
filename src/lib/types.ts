export interface Photo {
  url: string;
  description: string;
  date: string;
  location: string;
  /** Grid-sized local thumbnail, see scripts/generate_thumbs.py */
  thumb: string;
  /** Page-sized local render, see scripts/generate_thumbs.py */
  large: string;
  /** Intrinsic size of `thumb`, so layout space can be reserved before it loads */
  w: number;
  h: number;
}
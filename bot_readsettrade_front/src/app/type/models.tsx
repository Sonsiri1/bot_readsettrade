export interface AnalystColumn {
  id: number;
  symbol: string;
  broker: string;
  analyst: string;

  target_price: number | null;

  upside_value: number | null;
  upside_text: string | null;

  recommendation: string | null;
  report_date: string | null;

  company: {
    company_name: string;
    sector: string;
    industry: string;
  } | null;
};
 
export interface DetailAnalyst {
  id: number;
  symbol: string;
  broker: string;
  analyst: string | null;

  eps_2569: number | null;
  eps_2570: number | null;

  profit_2569: number | null;
  profit_2570: number | null;

  pe_2569: number | null;
  pe_2570: number | null;

  pbv_2569: number | null;
  pbv_2570: number | null;

  dividend_2569: number | null;
  dividend_2570: number | null;

  target_price: number | null;

  upside_value: number | null;
  upside_text: string | null;

  recommendation: string | null;

  report_date: string | null;
};
 
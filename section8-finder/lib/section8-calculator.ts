/**
 * Section 8 Cash-on-Cash Return Calculator
 * Polk County, FL — 3BR FMR: $1,797/mo
 */

export interface PropertyInput {
  price: number;
  bedrooms: number;
  bathrooms: number;
  sqft: number;
  yearBuilt: number;
  zip: string;
  hoa?: number;
}

export interface FinancingInput {
  downPaymentPercent: number; // Default: 20%
  interestRate: number; // Default: 6.11% (current 30yr)
  loanTermYears: number; // Default: 30
  propertyTaxRate: number; // Default: 1.25% (Polk County)
  insuranceAnnual: number; // Default: $1,800
  vacancyRate: number; // Default: 5%
  repairsCapexRate: number; // Default: 10%
  propertyMgmtRate: number; // Default: 8% (or 0 if self-managed)
}

export interface PropertyAnalysis {
  // Input
  purchasePrice: number;
  bedrooms: number;
  
  // FMR
  fmr: number;
  tenantPortion: number; // Typically 30%
  hapPayment: number; // Housing Assistance Payment (70%)
  
  // Financing
  downPayment: number;
  loanAmount: number;
  monthlyPI: number;
  
  // Monthly Expenses
  propertyTax: number;
  insurance: number;
  hoa: number;
  vacancy: number;
  repairsCapex: number;
  propertyMgmt: number;
  totalExpenses: number;
  
  // Cash Flow
  grossIncome: number;
  netCashFlow: number;
  annualCashFlow: number;
  
  // Returns
  cashOnCash: number; // % return on down payment
  capRate: number; // NOI / purchase price
  dealScore: number; // 0-100 based on multiple factors
  dealGrade: 'A+' | 'A' | 'B+' | 'B' | 'C' | 'D' | 'F';
  
  // Recommendations
  isGoodDeal: boolean;
  warnings: string[];
  improvements: string[];
}

/**
 * HUD Fair Market Rents for Polk County (Lakeland-Winter Haven MSA)
 * Source: HUD FY2025
 */
const POLK_FMR: Record<number, number> = {
  0: 1085, // Studio
  1: 1092, // 1BR
  2: 1337, // 2BR
  3: 1797, // 3BR
  4: 2245, // 4BR
};

/**
 * Default financing assumptions
 */
export const DEFAULT_FINANCING: FinancingInput = {
  downPaymentPercent: 20,
  interestRate: 6.11,
  loanTermYears: 30,
  propertyTaxRate: 1.25, // Polk County average
  insuranceAnnual: 1800, // FL homeowners average
  vacancyRate: 5, // Section 8 = lower vacancy
  repairsCapexRate: 10, // Conservative for older homes
  propertyMgmtRate: 8, // Or 0 if self-managed
};

/**
 * Calculate monthly mortgage payment (P&I only)
 */
function calculateMortgage(principal: number, annualRate: number, years: number): number {
  const monthlyRate = annualRate / 100 / 12;
  const numPayments = years * 12;
  
  if (monthlyRate === 0) return principal / numPayments;
  
  return (
    principal *
    (monthlyRate * Math.pow(1 + monthlyRate, numPayments)) /
    (Math.pow(1 + monthlyRate, numPayments) - 1)
  );
}

/**
 * Analyze a property for Section 8 investment potential
 */
export function analyzeProperty(
  property: PropertyInput,
  financing: FinancingInput = DEFAULT_FINANCING
): PropertyAnalysis {
  // Get FMR for bedroom count
  const fmr = POLK_FMR[property.bedrooms] || 0;
  if (fmr === 0) {
    throw new Error(`Unsupported bedroom count: ${property.bedrooms}`);
  }
  
  // Calculate FMR split (typically tenant pays 30%)
  const tenantPortion = fmr * 0.3;
  const hapPayment = fmr - tenantPortion;
  
  // Financing
  const downPayment = property.price * (financing.downPaymentPercent / 100);
  const loanAmount = property.price - downPayment;
  const monthlyPI = calculateMortgage(loanAmount, financing.interestRate, financing.loanTermYears);
  
  // Monthly expenses
  const propertyTax = (property.price * (financing.propertyTaxRate / 100)) / 12;
  const insurance = financing.insuranceAnnual / 12;
  const hoa = property.hoa || 0;
  const vacancy = fmr * (financing.vacancyRate / 100);
  const repairsCapex = fmr * (financing.repairsCapexRate / 100);
  const propertyMgmt = fmr * (financing.propertyMgmtRate / 100);
  
  const totalExpenses = monthlyPI + propertyTax + insurance + hoa + vacancy + repairsCapex + propertyMgmt;
  
  // Cash flow
  const grossIncome = fmr;
  const netCashFlow = grossIncome - totalExpenses;
  const annualCashFlow = netCashFlow * 12;
  
  // Returns
  const cashOnCash = (annualCashFlow / downPayment) * 100;
  const noi = (grossIncome - (propertyTax + insurance + hoa + vacancy + repairsCapex + propertyMgmt)) * 12;
  const capRate = (noi / property.price) * 100;
  
  // Deal scoring (0-100)
  let dealScore = 0;
  const warnings: string[] = [];
  const improvements: string[] = [];
  
  // Factor 1: Cash-on-Cash Return (40 points max)
  if (cashOnCash >= 12) dealScore += 40;
  else if (cashOnCash >= 10) dealScore += 35;
  else if (cashOnCash >= 8) dealScore += 30;
  else if (cashOnCash >= 6) dealScore += 20;
  else if (cashOnCash >= 4) dealScore += 10;
  
  if (cashOnCash < 5) warnings.push('Low cash-on-cash return (<5%). Negotiate lower price or self-manage.');
  if (cashOnCash < 8 && financing.propertyMgmtRate > 0) {
    improvements.push(`Self-manage to boost COC from ${cashOnCash.toFixed(1)}% to ${((annualCashFlow + (fmr * financing.propertyMgmtRate / 100 * 12)) / downPayment * 100).toFixed(1)}%`);
  }
  
  // Factor 2: Purchase Price (20 points max)
  if (property.price <= 165000) dealScore += 20;
  else if (property.price <= 180000) dealScore += 15;
  else if (property.price <= 200000) dealScore += 10;
  else if (property.price <= 220000) dealScore += 5;
  
  if (property.price > 200000) warnings.push('Price above sweet spot ($150K-$200K). Reduces cash flow.');
  
  // Factor 3: Property Age (15 points max)
  const age = 2026 - property.yearBuilt;
  if (age <= 10) dealScore += 15;
  else if (age <= 20) dealScore += 12;
  else if (age <= 30) dealScore += 8;
  else if (age <= 40) dealScore += 4;
  
  if (property.yearBuilt < 1990) warnings.push('Built before 1990 — higher HQS inspection risk (lead paint, old systems).');
  if (age > 30) improvements.push('Budget extra 2-3% for CapEx reserves (aging home).');
  
  // Factor 4: Neighborhood Tier (15 points max)
  const goodZips = ['33813', '33803', '33881', '33844']; // Lakeland East, Winter Haven East, Haines City North
  const okZips = ['33801', '33880', '33859', '33837']; // Bartow, Auburndale, etc.
  
  if (goodZips.includes(property.zip)) dealScore += 15;
  else if (okZips.includes(property.zip)) dealScore += 8;
  else dealScore += 3;
  
  // Factor 5: HOA (10 points max — no HOA is best)
  if (!property.hoa || property.hoa === 0) dealScore += 10;
  else if (property.hoa < 50) dealScore += 5;
  
  if (property.hoa && property.hoa > 0) {
    warnings.push(`HOA fee $${property.hoa}/mo reduces cash flow by $${property.hoa * 12}/yr. Many HOAs ban Section 8.`);
  }
  
  // Deal grade
  let dealGrade: PropertyAnalysis['dealGrade'] = 'F';
  if (dealScore >= 90) dealGrade = 'A+';
  else if (dealScore >= 80) dealGrade = 'A';
  else if (dealScore >= 70) dealGrade = 'B+';
  else if (dealScore >= 60) dealGrade = 'B';
  else if (dealScore >= 50) dealGrade = 'C';
  else if (dealScore >= 40) dealGrade = 'D';
  
  const isGoodDeal = cashOnCash >= 8 && dealScore >= 60;
  
  return {
    // Input
    purchasePrice: property.price,
    bedrooms: property.bedrooms,
    
    // FMR
    fmr,
    tenantPortion,
    hapPayment,
    
    // Financing
    downPayment,
    loanAmount,
    monthlyPI,
    
    // Monthly Expenses
    propertyTax,
    insurance,
    hoa,
    vacancy,
    repairsCapex,
    propertyMgmt,
    totalExpenses,
    
    // Cash Flow
    grossIncome,
    netCashFlow,
    annualCashFlow,
    
    // Returns
    cashOnCash,
    capRate,
    dealScore,
    dealGrade,
    
    // Recommendations
    isGoodDeal,
    warnings,
    improvements,
  };
}

/**
 * Format currency
 */
export function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
}

/**
 * Format percentage
 */
export function formatPercent(value: number, decimals: number = 1): string {
  return `${value.toFixed(decimals)}%`;
}

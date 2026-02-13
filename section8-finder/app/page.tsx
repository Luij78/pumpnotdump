'use client';

import { useState } from 'react';
import { analyzeProperty, formatCurrency, formatPercent, DEFAULT_FINANCING, type PropertyInput, type FinancingInput, type PropertyAnalysis } from '@/lib/section8-calculator';

export default function Home() {
  const [property, setProperty] = useState<PropertyInput>({
    price: 180000,
    bedrooms: 3,
    bathrooms: 2,
    sqft: 1400,
    yearBuilt: 2005,
    zip: '33813', // Lakeland East
    hoa: 0,
  });

  const [financing, setFinancing] = useState<FinancingInput>(DEFAULT_FINANCING);
  const [analysis, setAnalysis] = useState<PropertyAnalysis | null>(null);

  const handleAnalyze = () => {
    try {
      const result = analyzeProperty(property, financing);
      setAnalysis(result);
    } catch (error) {
      alert(error instanceof Error ? error.message : 'Analysis failed');
    }
  };

  // Auto-analyze on mount
  if (!analysis) {
    handleAnalyze();
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
      {/* Header */}
      <div className="border-b border-slate-700 bg-slate-900/50 backdrop-blur">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-400">
            Section 8 Property Finder
          </h1>
          <p className="text-slate-400 mt-1">Polk County, FL — Find 8%+ Cash-on-Cash Deals</p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8 grid md:grid-cols-2 gap-8">
        {/* Input Form */}
        <div className="space-y-6">
          <div className="bg-slate-800/50 backdrop-blur border border-slate-700 rounded-xl p-6">
            <h2 className="text-xl font-semibold mb-4 text-emerald-400">Property Details</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1">Purchase Price</label>
                <input
                  type="number"
                  value={property.price}
                  onChange={(e) => setProperty({ ...property, price: Number(e.target.value) })}
                  className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-2 text-white focus:border-emerald-500 focus:outline-none"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-1">Bedrooms</label>
                  <select
                    value={property.bedrooms}
                    onChange={(e) => setProperty({ ...property, bedrooms: Number(e.target.value) })}
                    className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-2 text-white focus:border-emerald-500 focus:outline-none"
                  >
                    <option value={1}>1 BR</option>
                    <option value={2}>2 BR</option>
                    <option value={3}>3 BR</option>
                    <option value={4}>4 BR</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-1">Bathrooms</label>
                  <input
                    type="number"
                    step="0.5"
                    value={property.bathrooms}
                    onChange={(e) => setProperty({ ...property, bathrooms: Number(e.target.value) })}
                    className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-2 text-white focus:border-emerald-500 focus:outline-none"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-1">Sqft</label>
                  <input
                    type="number"
                    value={property.sqft}
                    onChange={(e) => setProperty({ ...property, sqft: Number(e.target.value) })}
                    className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-2 text-white focus:border-emerald-500 focus:outline-none"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-1">Year Built</label>
                  <input
                    type="number"
                    value={property.yearBuilt}
                    onChange={(e) => setProperty({ ...property, yearBuilt: Number(e.target.value) })}
                    className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-2 text-white focus:border-emerald-500 focus:outline-none"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-1">ZIP Code</label>
                  <input
                    type="text"
                    value={property.zip}
                    onChange={(e) => setProperty({ ...property, zip: e.target.value })}
                    className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-2 text-white focus:border-emerald-500 focus:outline-none"
                    placeholder="33813"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-1">HOA ($/mo)</label>
                  <input
                    type="number"
                    value={property.hoa || 0}
                    onChange={(e) => setProperty({ ...property, hoa: Number(e.target.value) })}
                    className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-2 text-white focus:border-emerald-500 focus:outline-none"
                  />
                </div>
              </div>
            </div>
          </div>

          <div className="bg-slate-800/50 backdrop-blur border border-slate-700 rounded-xl p-6">
            <h2 className="text-xl font-semibold mb-4 text-cyan-400">Financing & Assumptions</h2>
            
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-1">Down Payment %</label>
                  <input
                    type="number"
                    value={financing.downPaymentPercent}
                    onChange={(e) => setFinancing({ ...financing, downPaymentPercent: Number(e.target.value) })}
                    className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-2 text-white focus:border-cyan-500 focus:outline-none"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-1">Interest Rate %</label>
                  <input
                    type="number"
                    step="0.01"
                    value={financing.interestRate}
                    onChange={(e) => setFinancing({ ...financing, interestRate: Number(e.target.value) })}
                    className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-2 text-white focus:border-cyan-500 focus:outline-none"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1">Property Mgmt % (0 = self-manage)</label>
                <input
                  type="number"
                  value={financing.propertyMgmtRate}
                  onChange={(e) => setFinancing({ ...financing, propertyMgmtRate: Number(e.target.value) })}
                  className="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-2 text-white focus:border-cyan-500 focus:outline-none"
                />
              </div>
            </div>
          </div>

          <button
            onClick={handleAnalyze}
            className="w-full bg-gradient-to-r from-emerald-500 to-cyan-500 text-white font-semibold py-3 rounded-lg hover:from-emerald-600 hover:to-cyan-600 transition"
          >
            Analyze Deal
          </button>
        </div>

        {/* Analysis Results */}
        {analysis && (
          <div className="space-y-6">
            {/* Deal Score */}
            <div className="bg-slate-800/50 backdrop-blur border border-slate-700 rounded-xl p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold text-white">Deal Score</h2>
                <div className={`text-3xl font-bold ${
                  analysis.dealGrade === 'A+' || analysis.dealGrade === 'A' ? 'text-emerald-400' :
                  analysis.dealGrade === 'B+' || analysis.dealGrade === 'B' ? 'text-cyan-400' :
                  analysis.dealGrade === 'C' ? 'text-yellow-400' :
                  'text-red-400'
                }`}>
                  {analysis.dealGrade}
                </div>
              </div>
              <div className="w-full bg-slate-700 rounded-full h-4 mb-2">
                <div 
                  className={`h-4 rounded-full ${
                    analysis.dealScore >= 80 ? 'bg-emerald-500' :
                    analysis.dealScore >= 60 ? 'bg-cyan-500' :
                    analysis.dealScore >= 40 ? 'bg-yellow-500' :
                    'bg-red-500'
                  }`}
                  style={{ width: `${analysis.dealScore}%` }}
                />
              </div>
              <p className="text-sm text-slate-400">{analysis.dealScore}/100 points</p>
              
              {analysis.isGoodDeal && (
                <div className="mt-4 bg-emerald-500/20 border border-emerald-500 rounded-lg p-3">
                  <p className="text-emerald-300 font-medium">✓ GOOD DEAL — 8%+ COC & 60+ Score</p>
                </div>
              )}
            </div>

            {/* Key Metrics */}
            <div className="bg-slate-800/50 backdrop-blur border border-slate-700 rounded-xl p-6">
              <h2 className="text-xl font-semibold mb-4 text-white">Key Metrics</h2>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-slate-300">Cash-on-Cash Return</span>
                  <span className="text-2xl font-bold text-emerald-400">{formatPercent(analysis.cashOnCash)}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-300">Annual Cash Flow</span>
                  <span className="text-xl font-semibold text-white">{formatCurrency(analysis.annualCashFlow)}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-300">Monthly Cash Flow</span>
                  <span className="text-lg text-slate-200">{formatCurrency(analysis.netCashFlow)}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-300">Cap Rate</span>
                  <span className="text-lg text-cyan-400">{formatPercent(analysis.capRate)}</span>
                </div>
              </div>
            </div>

            {/* Income & Expenses */}
            <div className="bg-slate-800/50 backdrop-blur border border-slate-700 rounded-xl p-6">
              <h2 className="text-xl font-semibold mb-4 text-white">Monthly Breakdown</h2>
              
              <div className="space-y-2 mb-4">
                <h3 className="font-medium text-emerald-400 mb-2">Income</h3>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-300">Section 8 FMR ({analysis.bedrooms}BR)</span>
                  <span className="text-white">{formatCurrency(analysis.fmr)}</span>
                </div>
                <div className="flex justify-between text-xs pl-4">
                  <span className="text-slate-400">HAP (Gov. pays)</span>
                  <span className="text-slate-300">{formatCurrency(analysis.hapPayment)}</span>
                </div>
                <div className="flex justify-between text-xs pl-4">
                  <span className="text-slate-400">Tenant portion (30%)</span>
                  <span className="text-slate-300">{formatCurrency(analysis.tenantPortion)}</span>
                </div>
              </div>

              <div className="space-y-2">
                <h3 className="font-medium text-red-400 mb-2">Expenses</h3>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-300">Mortgage P&I</span>
                  <span className="text-white">{formatCurrency(analysis.monthlyPI)}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-300">Property Tax</span>
                  <span className="text-white">{formatCurrency(analysis.propertyTax)}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-300">Insurance</span>
                  <span className="text-white">{formatCurrency(analysis.insurance)}</span>
                </div>
                {analysis.hoa > 0 && (
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-300">HOA</span>
                    <span className="text-white">{formatCurrency(analysis.hoa)}</span>
                  </div>
                )}
                <div className="flex justify-between text-sm">
                  <span className="text-slate-300">Vacancy (5%)</span>
                  <span className="text-white">{formatCurrency(analysis.vacancy)}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-300">Repairs/CapEx (10%)</span>
                  <span className="text-white">{formatCurrency(analysis.repairsCapex)}</span>
                </div>
                {analysis.propertyMgmt > 0 && (
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-300">Property Mgmt (8%)</span>
                    <span className="text-white">{formatCurrency(analysis.propertyMgmt)}</span>
                  </div>
                )}
                <div className="border-t border-slate-600 pt-2 flex justify-between text-sm font-semibold">
                  <span className="text-slate-200">Total Expenses</span>
                  <span className="text-white">{formatCurrency(analysis.totalExpenses)}</span>
                </div>
              </div>
            </div>

            {/* Warnings & Improvements */}
            {(analysis.warnings.length > 0 || analysis.improvements.length > 0) && (
              <div className="bg-slate-800/50 backdrop-blur border border-slate-700 rounded-xl p-6">
                <h2 className="text-xl font-semibold mb-4 text-white">Recommendations</h2>
                
                {analysis.warnings.length > 0 && (
                  <div className="mb-4">
                    <h3 className="text-sm font-medium text-yellow-400 mb-2">⚠️ Warnings</h3>
                    <ul className="space-y-1">
                      {analysis.warnings.map((warning, i) => (
                        <li key={i} className="text-sm text-slate-300 pl-4">• {warning}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {analysis.improvements.length > 0 && (
                  <div>
                    <h3 className="text-sm font-medium text-cyan-400 mb-2">💡 Improvements</h3>
                    <ul className="space-y-1">
                      {analysis.improvements.map((improvement, i) => (
                        <li key={i} className="text-sm text-slate-300 pl-4">• {improvement}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="max-w-7xl mx-auto px-4 py-8 text-center text-slate-400 text-sm border-t border-slate-700 mt-8">
        <p>Built by Skipper for Luis Garcia — Polk County Section 8 Investment Tool</p>
        <p className="mt-1">HUD FY2025 FMR Data • Polk County (Lakeland-Winter Haven MSA)</p>
      </div>
    </div>
  );
}

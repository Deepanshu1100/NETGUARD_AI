import { useState } from 'react'
import axios from 'axios'
import NetworkGraph from './NetworkGraph'
import { Activity, Cpu, Terminal, Users, Settings, ShieldAlert } from 'lucide-react'

function App() {
  // 1. DYNAMIC STATE
  // Yeh array network topology graph ko control karta hai
  const [nodes] = useState([1, 5, 12, 45, 10, 88, 92, 118, 150]);
  
  // Yeh state user input (Operations Console) ko handle karti hai
  const [formData, setFormData] = useState({
    location: 92,
    severity_type: 2,
    num_events: 100,
    total_log_volume: 5000
  });

  const [prediction, setPrediction] = useState(null);
  const [copilotData, setCopilotData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [userRole, setUserRole] = useState("L1 Engineer");

  const runAnalysis = async () => {
    setLoading(true);
    
    // 2. Payload ab hardcoded nahi hai, form se aa raha hai
    const payload = {
        location: parseInt(formData.location),
        severity_type: parseInt(formData.severity_type),
        num_events: parseInt(formData.num_events),
        total_log_volume: parseInt(formData.total_log_volume),
        num_resources: 5 // Default value
    };
    
    try {
      // Send data to XGBoost
      const predRes = await axios.post('http://127.0.0.1:8000/predict', payload)
      setPrediction(predRes.data)
      
      // Agar fault aata hai, tabhi Gemini AI ko trigger karo
      if (predRes.data.fault_severity > 0) {
        const copilotRes = await axios.post('http://127.0.0.1:8000/copilot', {
            role: userRole,
            fault_severity: predRes.data.fault_severity,
            location: formData.location.toString()
        })
        setCopilotData(copilotRes.data)
      } else {
        setCopilotData(null)
      }
    } catch (e) { 
        console.error("Error connecting to backend: ", e) 
    }
    
    setLoading(false)
  }

  return (
    <div className="min-h-screen p-8 font-mono bg-dark text-white">
      <h1 className="text-3xl font-bold mb-8 text-primary border-b border-slate-700 pb-4 flex items-center gap-3">
        <Activity className="w-8 h-8" />
        NETGUARD_AI COMMAND CENTER
      </h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* LEFT COLUMN: OPERATIONAL CONSOLE (Input Panel) */}
        <div className="bg-panel p-6 rounded-lg border border-slate-700 h-fit shadow-xl">
           <h2 className="flex items-center gap-2 mb-6 font-bold text-slate-300 border-b border-slate-700 pb-2">
             <Settings className="w-5 h-5"/> NETWORK INJECTOR
           </h2>
           
           <div className="space-y-4 text-sm">
             <div>
                <label className="text-slate-400 mb-1 block">Target Node ID:</label>
                <input 
                  type="number" 
                  value={formData.location} 
                  className="w-full bg-dark border border-slate-600 p-2 rounded outline-none focus:border-primary text-primary font-bold" 
                  onChange={(e) => setFormData({...formData, location: e.target.value})} 
                />
             </div>
             
             <div>
                <label className="text-slate-400 mb-1 block">Log Volume Burst:</label>
                <input 
                  type="number" 
                  value={formData.total_log_volume} 
                  className="w-full bg-dark border border-slate-600 p-2 rounded outline-none focus:border-primary text-primary font-bold" 
                  onChange={(e) => setFormData({...formData, total_log_volume: e.target.value})} 
                />
             </div>

             <div>
                <label className="text-slate-400 mb-1 block">Simulated Threat Level:</label>
                <select 
                  value={formData.severity_type}
                  className="w-full bg-dark border border-slate-600 p-2 rounded outline-none focus:border-primary text-primary font-bold" 
                  onChange={(e) => setFormData({...formData, severity_type: e.target.value})}
                >
                    <option value="0">Normal (0)</option>
                    <option value="1">Warning (1)</option>
                    <option value="2">Critical (2)</option>
                </select>
             </div>
             
             <button 
                onClick={runAnalysis} 
                disabled={loading} 
                className="w-full bg-primary hover:bg-blue-600 py-3 rounded font-bold text-dark mt-6 transition-all shadow-[0_0_15px_rgba(56,189,248,0.4)]"
             >
                {loading ? 'PROCESSING ML & AI...' : 'EXECUTE ANALYTICS'}
             </button>
           </div>
        </div>

        {/* RIGHT COLUMN: TOPOLOGY & AI OUTPUT */}
        <div className="lg:col-span-2 space-y-6">
           
           {/* XGBoost Status Bar */}
           <div className="bg-panel p-5 rounded-lg border border-slate-700 shadow-xl flex gap-6 items-center">
            <Cpu className="w-10 h-10 text-slate-500" />
            <div>
              <p className="text-slate-400 text-sm">XGBoost ML Engine Status</p>
              {prediction ? (
                <div className="mt-1 flex items-center gap-4">
                  <div>
                    <span className="text-lg font-bold">Severity: </span>
                    <span className={`text-xl font-extrabold ${prediction.fault_severity === 0 ? 'text-green-500' : prediction.fault_severity === 1 ? 'text-warning' : 'text-danger'}`}>
                      {prediction.fault_severity}
                    </span>
                  </div>
                  <span className="text-sm text-slate-400 border-l border-slate-600 pl-4">Confidence: {prediction.confidence}%</span>
                </div>
              ) : (
                <p className="text-sm mt-1 text-slate-500">System idle. Awaiting command execution...</p>
              )}
            </div>
          </div>

           {/* Network Graph Component */}
           <NetworkGraph 
             nodes={nodes} 
             faultLocation={formData.location} 
             severity={prediction?.fault_severity || 0} 
           />
           
           {/* AI Copilot Result Area */}
           <div className="bg-panel p-6 border border-slate-700 rounded-lg shadow-xl min-h-[200px]">
              <div className="flex justify-between items-center mb-4 border-b border-slate-700 pb-2">
                  <h3 className="text-primary font-bold flex items-center gap-2">
                    <Terminal className="w-5 h-5"/> AI COPILOT ANALYSIS
                  </h3>
                  <div className="flex items-center gap-2 bg-dark px-2 py-1 rounded border border-slate-600">
                    <Users className="w-4 h-4 text-slate-400" />
                    <select 
                      value={userRole} 
                      onChange={(e) => setUserRole(e.target.value)} 
                      className="bg-transparent border-none p-1 rounded text-xs text-primary outline-none cursor-pointer"
                    >
                        <option value="L1 Engineer">View as: L1 Engineer</option>
                        <option value="NOC Manager">View as: NOC Manager</option>
                    </select>
                  </div>
              </div>
              
              {loading && <p className="text-primary animate-pulse text-sm">Analyzing telemetry and generating report...</p>}
              
              {copilotData && !loading && (
                <div className="space-y-4">
                  <div className="bg-dark p-4 rounded border border-danger/30 flex items-start gap-3">
                    <ShieldAlert className="text-danger w-6 h-6 mt-1 flex-shrink-0" />
                    <p className="text-sm leading-relaxed text-slate-200">{copilotData.analysis}</p>
                  </div>
                  
                  <div className="mt-4 flex flex-wrap gap-3">
                      {copilotData.actions?.map((action, idx) => (
                        <button key={idx} className="bg-dark border border-slate-600 hover:border-primary text-xs px-4 py-2 rounded shadow-md transition-all text-slate-300 hover:text-primary">
                          {action.label}
                        </button>
                      ))}
                  </div>
                </div>
              )}

              {!copilotData && !loading && prediction?.fault_severity === 0 && (
                <p className="text-sm text-green-500">Network traffic normal. No Copilot intervention required.</p>
              )}
              
              {!copilotData && !loading && !prediction && (
                <p className="text-sm text-slate-500">Execute analytics to generate insights.</p>
              )}
           </div>
        </div>
      </div>
    </div>
  )
}

export default App
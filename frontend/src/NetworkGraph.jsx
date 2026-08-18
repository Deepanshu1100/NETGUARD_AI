// src/NetworkGraph.jsx
import { Server, Zap } from 'lucide-react'

const NetworkGraph = ({ nodes, faultLocation, severity }) => {
  return (
    <div className="bg-panel p-6 rounded-lg border border-slate-700 shadow-xl overflow-x-auto">
      <h2 className="text-sm font-bold text-slate-400 mb-6 uppercase tracking-widest">Live Network Topology</h2>
      
      {/* Dynamic mapping of nodes */}
      <div className="flex gap-4 min-w-max px-4">
        {nodes.map((nodeId) => {
          // Check if this specific node matches the injected fault location
          const isFaulty = parseInt(faultLocation) === nodeId && severity > 0;
          
          return (
            <div key={nodeId} className="flex flex-col items-center gap-2">
              <div className={`p-4 rounded-full border-2 transition-all ${isFaulty ? 'bg-danger/20 border-danger shadow-[0_0_20px_rgba(239,68,68,0.5)]' : 'bg-dark border-slate-600'}`}>
                {isFaulty ? <Zap className="w-6 h-6 text-danger animate-pulse" /> : <Server className="w-6 h-6 text-primary" />}
              </div>
              <span className="text-[10px] font-bold text-slate-400">NODE-{nodeId}</span>
            </div>
          )
        })}
      </div>
    </div>
  )
}

export default NetworkGraph
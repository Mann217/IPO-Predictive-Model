import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Srcc from '../components/srcc.jsx'
import MainTabs from '../components/MainTabs.jsx'

function App() {
  // Main React component for the IPOVision dashboard
  const [count, setCount] = useState(0)

  return (
    <>
      <div className="bg-black p-16 h-full">
        <MainTabs />

      </div>
    </>
  )
}

export default App

import { useState } from 'preact/hooks'
import './app.css'
import { Window } from './components/Window.jsx';

export function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
        <Window />
      </div>
      
    </>
  )
}

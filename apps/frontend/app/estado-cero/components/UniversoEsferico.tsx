'use client'

import { useRef, useMemo } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { Sphere, Box, Stars, OrbitControls } from '@react-three/drei'
import * as THREE from 'three'

interface UniversoEsfericoProps {
  fase: 'entrada' | 'expansion' | 'preguntas' | 'sintesis'
  momento?: string
}

function GeometriaSagrada({ fase }: { fase: string }) {
  const grupoRef = useRef<THREE.Group>(null)
  const esferaRef = useRef<THREE.Mesh>(null)
  const cuboRef = useRef<THREE.Mesh>(null)

  // Animación continua
  useFrame(({ clock }) => {
    const t = clock.getElapsedTime()
    
    if (grupoRef.current) {
      grupoRef.current.rotation.y = t * 0.1
    }

    if (esferaRef.current) {
      esferaRef.current.scale.setScalar(1 + Math.sin(t * 0.5) * 0.1)
    }

    if (cuboRef.current) {
      cuboRef.current.rotation.x = t * 0.3
      cuboRef.current.rotation.y = t * 0.2
    }
  })

  const colorFase = useMemo(() => {
    switch (fase) {
      case 'entrada': return '#8B5CF6' // Púrpura
      case 'expansion': return '#3B82F6' // Azul
      case 'preguntas': return '#22C55E' // Verde
      case 'sintesis': return '#A855F7' // Violeta
      default: return '#8B5CF6'
    }
  }, [fase])

  const mostrarEsfera = fase === 'entrada' || fase === 'expansion'
  const mostrarCubo = fase === 'preguntas' || fase === 'sintesis'

  return (
    <group ref={grupoRef}>
      {/* Esfera sagrada */}
      {mostrarEsfera && (
        <Sphere ref={esferaRef} args={[2, 32, 32]}>
          <meshStandardMaterial
            color={colorFase}
            wireframe
            transparent
            opacity={0.6}
          />
        </Sphere>
      )}

      {/* Cubo sagrado */}
      {mostrarCubo && (
        <Box ref={cuboRef} args={[2.5, 2.5, 2.5]}>
          <meshStandardMaterial
            color={colorFase}
            wireframe
            transparent
            opacity={0.7}
          />
        </Box>
      )}

      {/* Anillo de luz */}
      <mesh rotation={[Math.PI / 2, 0, 0]}>
        <torusGeometry args={[3, 0.05, 16, 100]} />
        <meshBasicMaterial color={colorFase} transparent opacity={0.3} />
      </mesh>
    </group>
  )
}

function ParticleField() {
  const particlesRef = useRef<THREE.Points>(null)

  const particlesPosition = useMemo(() => {
    const positions = new Float32Array(1000 * 3)
    
    for (let i = 0; i < 1000; i++) {
      const i3 = i * 3
      const radius = 10 + Math.random() * 10
      const theta = Math.random() * Math.PI * 2
      const phi = Math.random() * Math.PI
      
      positions[i3] = radius * Math.sin(phi) * Math.cos(theta)
      positions[i3 + 1] = radius * Math.sin(phi) * Math.sin(theta)
      positions[i3 + 2] = radius * Math.cos(phi)
    }
    
    return positions
  }, [])

  useFrame(({ clock }) => {
    if (particlesRef.current) {
      particlesRef.current.rotation.y = clock.getElapsedTime() * 0.02
    }
  })

  return (
    <points ref={particlesRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={particlesPosition.length / 3}
          array={particlesPosition}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial
        size={0.05}
        color="#ffffff"
        transparent
        opacity={0.6}
        sizeAttenuation
      />
    </points>
  )
}

export default function UniversoEsferico({ fase, momento }: UniversoEsfericoProps) {
  return (
    <div className="fixed inset-0 z-0">
      <Canvas
        camera={{ position: [0, 0, 8], fov: 60 }}
        gl={{ antialias: true, alpha: true }}
      >
        {/* Iluminación */}
        <ambientLight intensity={0.3} />
        <pointLight position={[10, 10, 10]} intensity={0.8} color="#8B5CF6" />
        <pointLight position={[-10, -10, -10]} intensity={0.5} color="#3B82F6" />

        {/* Estrellas de fondo */}
        <Stars
          radius={100}
          depth={50}
          count={5000}
          factor={4}
          saturation={0}
          fade
          speed={0.5}
        />

        {/* Campo de partículas */}
        <ParticleField />

        {/* Geometría sagrada principal */}
        <GeometriaSagrada fase={fase} />

        {/* Controles suaves (opcional, puede desactivarse) */}
        <OrbitControls
          enableZoom={false}
          enablePan={false}
          autoRotate
          autoRotateSpeed={0.5}
          maxPolarAngle={Math.PI / 1.5}
          minPolarAngle={Math.PI / 3}
        />
      </Canvas>
    </div>
  )
}


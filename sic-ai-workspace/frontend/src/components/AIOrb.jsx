import { Canvas, useFrame } from "@react-three/fiber";
import { Float, OrbitControls, Stars } from "@react-three/drei";
import { useRef } from "react";

function Orb() {
  const meshRef = useRef();

  useFrame((state, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.x += delta * 0.15;
      meshRef.current.rotation.y += delta * 0.25;
    }
  });

  return (
    <Float speed={2} rotationIntensity={1} floatIntensity={2}>
      <mesh ref={meshRef}>
        <icosahedronGeometry args={[2, 4]} />

        <meshStandardMaterial
          color="#7c3aed"
          emissive="#4f46e5"
          emissiveIntensity={1.5}
          wireframe
        />
      </mesh>
    </Float>
  );
}

export default function AIOrb() {
  return (
    <div style={{ width: "100%", height: "450px" }}>
      <Canvas camera={{ position: [0, 0, 6] }}>
        <ambientLight intensity={1} />

        <pointLight position={[5, 5, 5]} intensity={20} />

        <Stars
          radius={50}
          depth={20}
          count={600}
          factor={2}
          fade
          speed={1}
        />

        <Orb />

        <OrbitControls
          enableZoom={false}
          enablePan={false}
          autoRotate
          autoRotateSpeed={0.5}
        />
      </Canvas>
    </div>
  );
}
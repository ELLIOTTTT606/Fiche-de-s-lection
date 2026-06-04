// Fond animé subtil : orbes lumineux flottants + vagues SVG, mode clair/sombre.
export default function AnimatedBackground() {
  return (
    <div className="pointer-events-none fixed inset-0 -z-10 overflow-hidden">
      <div className="absolute -left-32 -top-32 h-96 w-96 animate-float rounded-full bg-electrique/20 blur-3xl" />
      <div
        className="absolute right-0 top-1/3 h-80 w-80 animate-float rounded-full bg-teal/20 blur-3xl"
        style={{ animationDelay: "1.5s" }}
      />
      <div
        className="absolute bottom-0 left-1/4 h-72 w-72 animate-float rounded-full bg-marine/20 blur-3xl"
        style={{ animationDelay: "3s" }}
      />
      <svg
        className="absolute bottom-0 left-0 w-full opacity-30 dark:opacity-20"
        viewBox="0 0 1440 320"
        preserveAspectRatio="none"
      >
        <path
          fill="#00a8e8"
          fillOpacity="0.4"
          d="M0,160 C320,260 720,60 1080,140 C1260,180 1380,200 1440,180 L1440,320 L0,320 Z"
        />
      </svg>
    </div>
  );
}

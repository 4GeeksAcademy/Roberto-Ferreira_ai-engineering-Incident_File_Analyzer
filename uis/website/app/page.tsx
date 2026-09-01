import { CompanyHighlights } from "@/components/company-highlights";
import { Hero } from "@/components/hero";
import { LocationsSection } from "@/components/locations-section";
import { SiteFooter } from "@/components/site-footer";
import { SiteHeader } from "@/components/site-header";

export default function HomePage() {
  return (
    <>
      <SiteHeader />
      <main>
        <Hero />
        <CompanyHighlights />
        <LocationsSection />
      </main>
      <SiteFooter />
    </>
  );
}

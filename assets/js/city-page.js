/**
 * city-page.js
 * Controller for city/sub-location pages within a geography.
 * Sets breadcrumb, city name, sidebar, and loads city content.
 */

class CityPage extends PageController {
  async setup(manifest) {
    const cityId = decodeURIComponent(this.currentId);
    const geoId  = decodeURIComponent(this.parentId);

    const geo  = manifest.geography.find(g => g.id === geoId);
    const city = geo && geo.locations.find(l => l.id === cityId);

    if (!geo || !city) {
      ContentLoader.showError(
        'city-name',
        'Location not found',
        `Could not find "${cityId}" within geography "${geoId}".`
      );
      return;
    }

    // Page metadata
    document.title = `${city.title} \u2014 Astatyr`;
    document.getElementById('city-name').textContent = city.title;
    document.getElementById('city-breadcrumb').textContent = city.title;

    // Breadcrumb country link
    const countryLink = document.getElementById('country-link');
    if (countryLink) {
      countryLink.textContent = geo.title;
      countryLink.href = `/worldbuilding/geography/${geoId}/`;
    }

    // Sidebar
    NavBuilder.forCity(geo, cityId);

    // City content
    await ContentLoader.load(
      `/generated/geography/${geoId}/${cityId}.html`,
      'city-content',
      `Add ${cityId}.docx to content/geography/${geoId}/ and wait for the Action.`
    );
  }
}
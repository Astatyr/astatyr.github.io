/**
 * location-page.js
 * Controller for top-level geography pages (countries/regions).
 * Shows overview content, type label, and cities grid.
 */

class LocationPage extends PageController {
  async setup(manifest) {
    const geoId = this.currentId === 'index' ? this.parentId : this.currentId;
    const geo = manifest.geography.find(g => g.id === geoId);

    if (!geo) {
      ContentLoader.showError(
        'loc-name',
        'Location not found',
        `No geography with id "${geoId}" exists in the manifest.`
      );
      return;
    }

    // Page metadata
    document.title = `${geo.title} \u2014 Astatyr`;
    document.getElementById('loc-name').textContent = geo.title;
    document.getElementById('loc-type').textContent = geo.type;

    // Sidebar
    NavBuilder.forGeography(manifest.geography, geoId);

    // Cities grid
    if (geo.locations && geo.locations.length > 0) {
      const section = document.getElementById('cities-section');
      const grid = document.getElementById('cities-grid');
      if (section) section.style.display = 'block';
      if (grid) {
        grid.innerHTML = geo.locations.map(loc => {
          const imgStyle = loc.image
            ? ` style="background-image: url(${loc.image})"`
            : '';
          return `
            <a class="loc-card" href="/worldbuilding/geography/${geoId}/${loc.id}.html">
              <div class="loc-img"${imgStyle}></div>
              <div class="loc-info">
                <div class="loc-type">Location</div>
                <div class="loc-name">${loc.title}</div>
              </div>
            </a>`;
        }).join('');
      }
    }

    // Overview content
    await ContentLoader.load(
      `/generated/geography/${geoId}/index.html`,
      'loc-content',
      `Add index.docx to content/geography/${geoId}/ to show an overview here.`
    );
  }
}

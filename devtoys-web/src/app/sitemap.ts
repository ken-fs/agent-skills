import { MetadataRoute } from 'next';

const BASE_URL = 'https://devtoys.io';

export default function sitemap(): MetadataRoute.Sitemap {
  const routes = [
    '',
    '/json-formatter',
    // We can add more specific tool routes here as they are developed
  ].map((route) => ({
    url: `${BASE_URL}${route}`,
    lastModified: new Date(),
    changeFrequency: 'weekly' as const,
    priority: route === '' ? 1 : 0.8,
  }));

  return routes;
}

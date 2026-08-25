import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('http://localhost:5173/');
  await page.getByRole('link', { name: 'Home' }).click();
  await page.getByText('Est. 2005 · Hyderabad, TelanganaWelcome to EduReach CollegeYour Gateway to').click();
  await page.getByText('EduReachHomeAboutCoursesMentorsCampusPlacementsLoginSign Up').click();
  await page.getByRole('link', { name: 'Campus', exact: true }).click();
});
Object.defineProperty(process, 'platform', { value: 'linux' });

const { chromium } = require('playwright-core');
const cheerio = require('cheerio');
require('dotenv/config');

class GtcAPI {
    constructor(context) {
        this.context = context;
        this.request = context.request; // shared session sama browser
        this.ec = null;
    }

    async initEc() {
        const page = await this.context.newPage();
        await page.goto('https://tools.naufalist.com/getcontact', { waitUntil: 'domcontentloaded' });
        await new Promise(r => setTimeout(r, 5000)); // kasih waktu script anti-bot jalan

        const html = await page.content();
        const ecMatch = html.match(/name="ec"\s+value="(.*?)"/);
        this.ec = ecMatch ? ecMatch[1] : null;

        await page.close();
        return this.ec;
    }

    async getToken() {
        try {
            const res = await this.request.get('https://cf-solver-three.vercel.app/api/gettoken');
            const data = await res.json();
            return data?.token ?? null;
        } catch {
            return null;
        }
    }

    async getCredent() {
        try {
            const credRes = await this.request.get('https://tools.naufalist.com/getcontact/api/credentials');
            const credData = await credRes.json();
            const key = credData?.data?.[0]?.id;

            const checkRes = await this.request.post(
                'https://tools.naufalist.com/getcontact/api/subscription',
                {
                    headers: {
                        'Origin': 'https://tools.naufalist.com',
                        'Content-Type': 'application/json',
                        'Referer': 'https://tools.naufalist.com/getcontact',
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                    data: { id: key },
                }
            );
            const checkData = await checkRes.json();

            const remaining = checkData?.data?.info?.search?.remainingCount;
            if (remaining === 0) return null;
            return key;
        } catch {
            return null;
        }
    }

    async gtcProfile(number, token, key) {
        try {
            if (!this.ec) throw new Error('ec belum diambil, panggil initEc() dulu');

            const r2 = await this.request.post('https://tools.naufalist.com/getcontact', {
                headers: {
                    'Origin': 'https://tools.naufalist.com',
                    'Referer': 'https://tools.naufalist.com/getcontact',
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                form: {
                    ec: this.ec,
                    phone_number: number,
                    credential: key,
                    source_type: 'search',
                    'cf-turnstile-response': token,
                },
            });

            const html = await r2.text();
            const $ = cheerio.load(html);

            const imgMatch = html.match(
                /<img(?=[^>]*alt=["']Profile Image["'])(?=[^>]*src=["']([^"']+)["'])[^>]*>/
            );
            const profileImage = imgMatch ? imgMatch[1] : null;

            const data = { profile_image: profileImage };

            $('dt').each((_, el) => {
                const dt = $(el);
                const dd = dt.next('dd');
                const key = dt.text().trim();
                const value = dd.length ? dd.text().trim() : null;
                data[key] = value;
            });

            if (!('Name' in data)) {
                return { message: 'data nomor tidak di temukan' };
            }
            return data;
        } catch {
            return { message: 'ada kesalahan pada sistem' };
        }
    }
}

(async () => {
    const browser = await chromium.launch({
        executablePath: process.env.CHROMIUM_PATH,
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
    });

    const context = await browser.newContext({
        viewport: { width: 1280, height: 800 },
        userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    });

    const client = new GtcAPI(context);

    console.log('🌐 Ambil ec dari halaman...');
    await client.initEc();
    console.log('ec:', client.ec);

    const token = await client.getToken();
    if (!token) {
        console.log(' ! token eror');
        await browser.close();
        return;
    }

    const credent = await client.getCredent();
    if (!credent) {
        console.log(' ! credentian eror');
        await browser.close();
        return;
    }

    const result = await client.gtcProfile('6282252139371', token, credent);
    console.log(JSON.stringify(result, null, 4));

    await browser.close();
})();

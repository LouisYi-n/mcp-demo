import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs';
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
// 定义 JSON 路径
console.log('当前工作目录:', process.cwd());
const JSON_PATH = path.join(process.cwd(), './citycodes.json');
let cityMappings = [];
// 读取 JSON 数据并存入内存
function loadCityMappings() {
    console.error('JSON_PATH:', JSON_PATH);
    if (!fs.existsSync(JSON_PATH)) {
        throw new Error(`文件不存在: ${JSON_PATH}`);
    }
    try {
        const data = fs.readFileSync(JSON_PATH, 'utf-8');
        const jsonData = JSON.parse(data);
        // 使用类型断言确保数据结构一致性
        cityMappings = jsonData.map(item => ({
            name: item.name.trim(),
            adcode: item.adcode.trim()
        }));
    }
    catch (error) {
        throw new Error(`JSON 解析失败: ${error instanceof Error ? error.message : String(error)}`);
    }
}
// 模糊搜索城市编码
function findAdcode(cityName) {
    const candidates = cityMappings.filter(item => item.name.startsWith(cityName));
    if (candidates.length === 0) {
        throw new Error('找不到城市');
    }
    if (candidates.length > 1) {
        throw new Error('请输入精确的地区名称');
    }
    return candidates[0].adcode;
}
export async function getCityAdcode(cityName) {
    if (cityMappings.length === 0) {
        loadCityMappings(); // 第一次调用时加载数据
    }
    try {
        return findAdcode(cityName.trim());
    }
    catch (error) {
        throw new Error(error.message);
    }
}

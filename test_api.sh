#!/bin/bash
# API 测试脚本

PORT=${1:-7860}
BASE_URL="http://localhost:${PORT}"

echo "========================================="
echo "  InfiniteTalk API 测试"
echo "========================================="
echo "测试地址: $BASE_URL"
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 测试函数
test_endpoint() {
    local name=$1
    local method=$2
    local endpoint=$3
    local data=$4
    
    echo -n "测试 $name ... "
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" "$BASE_URL$endpoint")
    else
        response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL$endpoint" $data)
    fi
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n-1)
    
    if [ "$http_code" = "200" ]; then
        echo -e "${GREEN}✓ 通过${NC}"
        echo "  响应: $(echo $body | head -c 100)..."
    else
        echo -e "${RED}✗ 失败 (HTTP $http_code)${NC}"
        echo "  响应: $body"
    fi
    echo ""
}

# 1. 健康检查
test_endpoint "健康检查" "GET" "/health"

# 2. GPU 状态
test_endpoint "GPU 状态" "GET" "/gpu/status"

# 3. 手动卸载
test_endpoint "手动卸载 GPU" "POST" "/gpu/offload"

# 4. 更新超时
test_endpoint "更新超时时间" "POST" "/gpu/timeout" "-F timeout=120"

# 5. Swagger 文档
echo -n "测试 Swagger 文档 ... "
if curl -s "$BASE_URL/docs" | grep -q "swagger"; then
    echo -e "${GREEN}✓ 通过${NC}"
else
    echo -e "${RED}✗ 失败${NC}"
fi
echo ""

# 6. 完全释放
test_endpoint "完全释放 GPU" "POST" "/gpu/release"

echo "========================================="
echo "  测试完成"
echo "========================================="
echo ""
echo "📍 访问地址:"
echo "   UI 界面:  $BASE_URL"
echo "   API 文档: $BASE_URL/docs"
echo ""

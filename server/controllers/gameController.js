/**
 * 获取全部游戏数据
 */
exports.getGames = async (req, res) => {
  try {
    const games = await Game.find(); // 恢复为获取全部游戏数据
    res.json(games);
  } catch (error) {
    res.status(500).json({ error: "获取游戏数据失败" });
  }
};
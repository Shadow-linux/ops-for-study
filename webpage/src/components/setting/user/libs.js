// 转换role
export const getRole = (name) => {
  if (name === '管理员') {
    return { 'is_staff': true, 'is_superuser': true }
  }
  if (name === '普通用户') {
    return { 'is_staff': true, 'is_superuser': false }
  }
  if (name === 'Guest') {
    return { 'is_staff': false, 'is_superuser': false }
  }
}

// 转换成gid
export const getGroup = (group, groupList) => {
  for (var idx in groupList) {
    if (group === groupList[idx]['name']) {
      return groupList[idx]['id']
    }
  }
}

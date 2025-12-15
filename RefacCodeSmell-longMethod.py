def generate_user_report(users):
    report = []
    title = "User Report"
    report.append(title)
    report.append("=" * len(title))
    for u in users:
        line = f"{u['id']}: {u['first_name']} {u['last_name']} <{u['email']}>"
        # format created date
        created = u.get('created_at')
        if created:
            created_str = created.strftime("%Y-%m-%d")
        else:
            created_str = "N/A"
        # compute status
        status = "active" if u.get('active', False) else "inactive"
        report.append(f"{line} | created: {created_str} | {status}")
    return "\n".join(report)
#Britannia Table Tennis Club, 193 Defoe Rd, Ipswich IP1 6SG
"""
Algorithm for dynamic adjusting of target probability.
"""


def compute_target_probability(target_success, correct_ratio, total_count):
    """
    Computes adjusted target probability, i.e. optimal probability of next
    exercise. Target probability is based on the desired 'target_sucess',
    but adjusted according to the actual success (if the user has higher
    actual success, we want to select more difficult question, and vice versa).
    """
    # correct ratio stabilization (to make the recommendations at the
    # beginning less influened by the success rate)
    stabilizator_weight = 1.0 / (0.25 * (total_count ** 2) + 1)
    actual_success = (1 - stabilizator_weight) * correct_ratio\
        + (stabilizator_weight * target_success)

    if actual_success >= target_success:
        slope = target_success / (1.0 - target_success)
        adjusted_target_success = slope * (1.0 - actual_success)
    else:
        slope = (1.0 - target_success) / target_success
        adjusted_target_success = 1.0 - slope * actual_success

    return adjusted_target_success
